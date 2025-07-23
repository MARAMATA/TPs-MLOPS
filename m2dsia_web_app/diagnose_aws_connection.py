# diagnose_aws_connection.py - Diagnostic de connexion AWS RDS
import socket
import subprocess
import sys
import os
import time
import pymysql
from sqlalchemy import create_engine, text

# Configuration AWS RDS
AWS_RDS_CONFIG = {
    "host": "m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com",
    "user": "root",
    "password": "rootM2dsia",
    "database": "m2dsia_maramata",
    "port": 3306
}

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print step with formatting"""
    print(f"\n{step}. {description}")
    print("-" * 50)

def test_internet_connectivity():
    """Test basic internet connectivity"""
    print_step("1", "Testing Internet Connectivity")
    
    try:
        # Test Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        print("✅ Internet connectivity: OK")
        return True
    except Exception as e:
        print(f"❌ Internet connectivity: FAILED - {e}")
        return False

def test_dns_resolution():
    """Test DNS resolution"""
    print_step("2", "Testing DNS Resolution")
    
    try:
        ip_address = socket.gethostbyname(AWS_RDS_CONFIG["host"])
        print(f"✅ DNS resolution: OK")
        print(f"   📍 Host: {AWS_RDS_CONFIG['host']}")
        print(f"   📍 IP: {ip_address}")
        return True, ip_address
    except Exception as e:
        print(f"❌ DNS resolution: FAILED - {e}")
        return False, None

def test_port_connectivity(ip_address=None):
    """Test port connectivity"""
    print_step("3", "Testing Port Connectivity")
    
    host = ip_address if ip_address else AWS_RDS_CONFIG["host"]
    port = AWS_RDS_CONFIG["port"]
    
    try:
        socket.create_connection((host, port), timeout=10)
        print(f"✅ Port connectivity: OK")
        print(f"   📍 Host: {host}:{port}")
        return True
    except Exception as e:
        print(f"❌ Port connectivity: FAILED - {e}")
        print(f"   📍 Host: {host}:{port}")
        return False

def test_mysql_connection():
    """Test direct MySQL connection"""
    print_step("4", "Testing MySQL Connection")
    
    try:
        connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL connection: OK")
            print(f"   📍 MySQL version: {version[0]}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ MySQL connection: FAILED - {e}")
        return False

def test_database_existence():
    """Test if database exists"""
    print_step("5", "Testing Database Existence")
    
    try:
        connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        with connection.cursor() as cursor:
            cursor.execute("SHOW DATABASES")
            databases = cursor.fetchall()
            db_names = [db[0] for db in databases]
            
            print(f"✅ Available databases: {len(db_names)}")
            for db in db_names:
                print(f"   📍 {db}")
                
            if AWS_RDS_CONFIG["database"] in db_names:
                print(f"✅ Target database '{AWS_RDS_CONFIG['database']}' exists")
                return True
            else:
                print(f"❌ Target database '{AWS_RDS_CONFIG['database']}' does not exist")
                return False
                
        connection.close()
        
    except Exception as e:
        print(f"❌ Database check: FAILED - {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    print_step("6", "Testing SQLAlchemy Connection")
    
    try:
        DATABASE_URL = (
            f"mysql+pymysql://{AWS_RDS_CONFIG['user']}:{AWS_RDS_CONFIG['password']}"
            f"@{AWS_RDS_CONFIG['host']}:{AWS_RDS_CONFIG['port']}/{AWS_RDS_CONFIG['database']}"
        )
        
        engine = create_engine(
            DATABASE_URL,
            pool_pre_ping=True,
            connect_args={
                "connect_timeout": 30,
                "read_timeout": 30,
                "write_timeout": 30
            }
        )
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print(f"✅ SQLAlchemy connection: OK")
            return True
            
    except Exception as e:
        print(f"❌ SQLAlchemy connection: FAILED - {e}")
        return False

def ping_host():
    """Ping the host"""
    print_step("7", "Pinging Host")
    
    try:
        # Try ping command
        result = subprocess.run(
            ["ping", "-c", "3", AWS_RDS_CONFIG["host"]], 
            capture_output=True, 
            text=True, 
            timeout=15
        )
        
        if result.returncode == 0:
            print(f"✅ Ping successful")
            print(f"   📍 Response: {result.stdout.split()[-1]}")
            return True
        else:
            print(f"❌ Ping failed")
            print(f"   📍 Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Ping test: FAILED - {e}")
        return False

def test_traceroute():
    """Test traceroute to host"""
    print_step("8", "Testing Route to Host")
    
    try:
        result = subprocess.run(
            ["traceroute", "-m", "10", AWS_RDS_CONFIG["host"]], 
            capture_output=True, 
            text=True, 
            timeout=30
        )
        
        print(f"📍 Traceroute to {AWS_RDS_CONFIG['host']}:")
        print(result.stdout)
        return True
        
    except Exception as e:
        print(f"❌ Traceroute test: FAILED - {e}")
        return False

def create_database_if_needed():
    """Create database if it doesn't exist"""
    print_step("9", "Creating Database if Needed")
    
    try:
        connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {AWS_RDS_CONFIG['database']}")
            cursor.execute(f"USE {AWS_RDS_CONFIG['database']}")
            print(f"✅ Database '{AWS_RDS_CONFIG['database']}' ready")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database creation: FAILED - {e}")
        return False

def main():
    """Main diagnostic function"""
    print_header("AWS RDS Connection Diagnostic")
    print(f"🎯 Target: {AWS_RDS_CONFIG['host']}:{AWS_RDS_CONFIG['port']}")
    print(f"🗄️  Database: {AWS_RDS_CONFIG['database']}")
    print(f"👤 User: {AWS_RDS_CONFIG['user']}")
    
    # Run all tests
    tests = [
        test_internet_connectivity,
        test_dns_resolution,
        lambda: test_port_connectivity(),
        test_mysql_connection,
        test_database_existence,
        test_sqlalchemy_connection,
        ping_host,
        test_traceroute,
        create_database_if_needed
    ]
    
    results = []
    
    for i, test in enumerate(tests, 1):
        try:
            if i == 2:  # Special handling for DNS resolution
                dns_ok, ip = test_dns_resolution()
                results.append(dns_ok)
                if dns_ok:
                    port_ok = test_port_connectivity(ip)
                    results.append(port_ok)
                else:
                    results.append(False)
                continue
            elif i == 3:  # Skip port test as it's handled above
                continue
            else:
                result = test()
                results.append(result)
        except Exception as e:
            print(f"❌ Test {i} failed with exception: {e}")
            results.append(False)
    
    # Summary
    print_header("DIAGNOSTIC SUMMARY")
    passed = sum(results)
    total = len(results)
    
    print(f"📊 Tests passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! AWS RDS should work.")
    elif passed >= total * 0.7:
        print("⚠️  MOST TESTS PASSED. AWS RDS should work with minor issues.")
    else:
        print("❌ MULTIPLE TESTS FAILED. AWS RDS connection has issues.")
    
    # Recommendations
    print_header("RECOMMENDATIONS")
    
    if not results[0]:  # Internet connectivity
        print("🔧 Fix internet connectivity first")
    elif not results[1]:  # DNS resolution
        print("🔧 Check DNS settings or use IP address directly")
    elif not results[2]:  # Port connectivity
        print("🔧 Check AWS security groups and network ACLs")
        print("🔧 Ensure port 3306 is open from your IP")
    elif not results[3]:  # MySQL connection
        print("🔧 Check AWS RDS instance status")
        print("🔧 Verify credentials and user permissions")
    elif not results[4]:  # Database existence
        print("🔧 Create the database manually or run the creation script")
    else:
        print("🔧 Connection should work. Try running the app again.")

if __name__ == "__main__":
    main()