# db/connexion.py - VERSION AWS RDS
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
import os
import socket
import time
import logging

# Configuration de base
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration AWS RDS
AWS_RDS_CONFIG = {
    "host": "m2dsia-mlops.cfuik82swe2y.eu-central-1.rds.amazonaws.com",
    "user": "root",
    "password": "rootM2dsia",
    "database": "m2dsia_maramata",
    "port": 3306
}

# Configuration SQLite locale (fallback)
LOCAL_DATABASE_URL = "sqlite:///./m2dsia_local.db"

def test_host_connectivity(host, port=3306, timeout=5):
    """Test if we can connect to the host"""
    try:
        socket.create_connection((host, port), timeout)
        logger.info(f"✅ Host {host}:{port} is reachable")
        return True
    except socket.error as e:
        logger.error(f"❌ Cannot reach {host}:{port} - {e}")
        return False

def test_dns_resolution(host):
    """Test DNS resolution"""
    try:
        socket.gethostbyname(host)
        logger.info(f"✅ DNS resolution successful for {host}")
        return True
    except socket.gaierror as e:
        logger.error(f"❌ DNS resolution failed for {host} - {e}")
        return False

def create_aws_engine():
    """Create AWS RDS MySQL engine"""
    try:
        # Test DNS resolution first
        if not test_dns_resolution(AWS_RDS_CONFIG["host"]):
            logger.error("DNS resolution failed, cannot connect to AWS RDS")
            return None
        
        # Test connectivity
        if not test_host_connectivity(AWS_RDS_CONFIG["host"], AWS_RDS_CONFIG["port"]):
            logger.error("Host connectivity failed, cannot connect to AWS RDS")
            return None
        
        # Create connection URL
        DATABASE_URL = (
            f"mysql+pymysql://{AWS_RDS_CONFIG['user']}:{AWS_RDS_CONFIG['password']}"
            f"@{AWS_RDS_CONFIG['host']}:{AWS_RDS_CONFIG['port']}/{AWS_RDS_CONFIG['database']}"
        )
        
        # Create engine with connection pooling and error handling
        engine = create_engine(
            DATABASE_URL,
            echo=True,
            pool_size=10,
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600,
            connect_args={
                "connect_timeout": 30,
                "read_timeout": 30,
                "write_timeout": 30,
                "charset": "utf8mb4"
            }
        )
        
        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ AWS RDS connection successful!")
            
        return engine
        
    except Exception as e:
        logger.error(f"❌ Failed to create AWS RDS engine: {e}")
        return None

def create_local_engine():
    """Create local SQLite engine as fallback"""
    try:
        engine = create_engine(
            LOCAL_DATABASE_URL,
            echo=True,
            connect_args={"check_same_thread": False}
        )
        
        # Test the connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            logger.info("✅ Local SQLite connection successful!")
            
        return engine
        
    except Exception as e:
        logger.error(f"❌ Failed to create local SQLite engine: {e}")
        return None

def get_engine():
    """Get database engine with fallback logic"""
    
    # Try to use environment variable first
    use_aws = os.getenv("USE_AWS_RDS", "true").lower() == "true"
    
    if use_aws:
        logger.info("🔄 Attempting to connect to AWS RDS...")
        engine = create_aws_engine()
        
        if engine:
            logger.info("🎉 Using AWS RDS MySQL database")
            return engine
        else:
            logger.warning("⚠️ AWS RDS connection failed, falling back to local SQLite")
    
    # Fallback to local SQLite
    logger.info("🔄 Using local SQLite database")
    return create_local_engine()

# Create engine with fallback
engine = get_engine()

if engine is None:
    raise Exception("❌ Failed to create any database engine!")

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()

# Dependency to get database session
def get_db():
    """
    Dependency function to get database session
    Use this in your FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Test connection function
def test_connection():
    """
    Test database connection
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            db_name = connection.execute(text("SELECT DATABASE()")).fetchone()
            if db_name and db_name[0]:
                logger.info(f"✅ Database connection successful! Connected to: {db_name[0]}")
            else:
                logger.info("✅ Database connection successful! (SQLite)")
            return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False

# Utility functions
def get_current_database_info():
    """Get current database information"""
    try:
        with engine.connect() as connection:
            if "sqlite" in str(engine.url):
                return {
                    "type": "SQLite",
                    "file": str(engine.url).replace("sqlite:///", ""),
                    "status": "Connected"
                }
            else:
                db_name = connection.execute(text("SELECT DATABASE()")).fetchone()
                return {
                    "type": "MySQL",
                    "host": AWS_RDS_CONFIG["host"],
                    "database": db_name[0] if db_name else "Unknown",
                    "status": "Connected"
                }
    except Exception as e:
        return {
            "type": "Unknown",
            "status": f"Error: {e}"
        }

def force_aws_connection():
    """Force reconnection to AWS RDS"""
    global engine, SessionLocal
    
    logger.info("🔄 Forcing AWS RDS connection...")
    engine = create_aws_engine()
    
    if engine:
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base.metadata.bind = engine
        logger.info("✅ Forced AWS RDS connection successful!")
        return True
    else:
        logger.error("❌ Failed to force AWS RDS connection")
        return False

if __name__ == "__main__":
    print("🔍 Database Connection Test")
    print("=" * 50)
    
    # Test connection
    if test_connection():
        info = get_current_database_info()
        print(f"📊 Database Info: {info}")
    
    # Show connection details
    print(f"\n🔧 Engine URL: {engine.url}")
    print(f"🔧 Engine Type: {type(engine).__name__}")