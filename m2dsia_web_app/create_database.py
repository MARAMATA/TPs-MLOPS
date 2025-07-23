# create_database.py
import pymysql
from sqlalchemy import create_engine, text

# Database connection parameters
host = "m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com"
user = "root"
password = "rootM2dsia"
database_name = "m2dsia_maramata"

def create_database_if_not_exists():
    """
    Create the database if it doesn't exist
    """
    try:
        # Connect to MySQL server without specifying a database
        connection_url = f"mysql+pymysql://{user}:{password}@{host}:3306"
        engine = create_engine(connection_url)
        
        # Create database if it doesn't exist
        with engine.connect() as connection:
            # Use text() to wrap the SQL statement
            connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database_name}"))
            connection.commit()
            print(f"✓ Database '{database_name}' created successfully or already exists!")
            
    except Exception as e:
        print(f"✗ Error creating database: {e}")
        return False
    
    return True

def test_database_connection():
    """
    Test connection to the created database
    """
    try:
        # Connect to the specific database
        connection_url = f"mysql+pymysql://{user}:{password}@{host}:3306/{database_name}"
        engine = create_engine(connection_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SELECT DATABASE()"))
            current_db = result.fetchone()[0]
            print(f"✓ Successfully connected to database: {current_db}")
            
    except Exception as e:
        print(f"✗ Error connecting to database: {e}")
        return False
    
    return True

def show_databases():
    """
    Show all databases
    """
    try:
        connection_url = f"mysql+pymysql://{user}:{password}@{host}:3306"
        engine = create_engine(connection_url)
        
        with engine.connect() as connection:
            result = connection.execute(text("SHOW DATABASES"))
            databases = result.fetchall()
            print("\n📋 Available databases:")
            for db in databases:
                print(f"  - {db[0]}")
                
    except Exception as e:
        print(f"✗ Error showing databases: {e}")

if __name__ == "__main__":
    print("🚀 Creating M2DSIA Database...")
    print("=" * 50)
    
    if create_database_if_not_exists():
        test_database_connection()
        show_databases()
        print("\n🎉 Database setup completed successfully!")
    else:
        print("\n❌ Database setup failed!")