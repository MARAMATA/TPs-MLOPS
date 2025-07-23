# setup_aws_database.py - VERSION CORRIGÉE
import sys
import os
import pymysql
from sqlalchemy import create_engine, text
import time

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Configuration AWS RDS - HOSTNAME CORRIGÉ
AWS_RDS_CONFIG = {
    "host": "m2dsia-mlops.cfuik82swe2y.eu-central-1.rds.amazonaws.com",  # CORRIGÉ !
    "user": "root",
    "password": "rootM2dsia",
    "database": "m2dsia_maramata",
    "port": 3306
}

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_step(step, description):
    """Print step with formatting"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def test_connection():
    """Test basic AWS RDS connection"""
    print_step("1", "Testing AWS RDS Connection")
    
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
            print(f"✅ AWS RDS connection successful!")
            print(f"   📍 MySQL version: {version[0]}")
            print(f"   🌐 Host: {AWS_RDS_CONFIG['host']}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ AWS RDS connection failed: {e}")
        return False

def create_database():
    """Create the database if it doesn't exist"""
    print_step("2", "Creating Database")
    
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
            print(f"✅ Database '{AWS_RDS_CONFIG['database']}' created successfully!")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Database creation failed: {e}")
        return False

def create_tables():
    """Create all tables using direct SQL"""
    print_step("3", "Creating Tables")
    
    try:
        connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            database=AWS_RDS_CONFIG["database"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        with connection.cursor() as cursor:
            # Create users table
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                nom VARCHAR(255) NOT NULL,
                prenom VARCHAR(255) NOT NULL,
                classe VARCHAR(255) NOT NULL,
                is_active BOOLEAN DEFAULT TRUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email),
                INDEX idx_id (id)
            );
            """
            
            cursor.execute(create_table_sql)
            
            # Show tables to verify
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"✅ Tables created successfully!")
            print(f"   📋 Tables found: {len(tables)}")
            for table in tables:
                print(f"      - {table[0]}")
            
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Table creation failed: {e}")
        return False

def add_sample_data():
    """Add sample data to AWS RDS"""
    print_step("4", "Adding Sample Data")
    
    try:
        connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            database=AWS_RDS_CONFIG["database"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        # Sample users data
        sample_users = [
            ("john.doe@isi.com", "Doe", "John", "MLOps 2025"),
            ("jane.smith@isi.com", "Smith", "Jane", "MLOps 2025"),
            ("lipson.soume@isi.com", "Soume", "Lipson", "MLOps 2025"),
            ("maramata.student@isi.com", "Maramata", "Student", "MLOps 2025"),
            ("aws.user@isi.com", "AWS", "User", "Cloud Computing 2025")
        ]
        
        with connection.cursor() as cursor:
            # Add users if they don't exist
            for email, nom, prenom, classe in sample_users:
                # Check if user exists
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    cursor.execute(
                        "INSERT INTO users (email, nom, prenom, classe) VALUES (%s, %s, %s, %s)",
                        (email, nom, prenom, classe)
                    )
                    print(f"✅ User {email} added successfully!")
                else:
                    print(f"⚠️  User {email} already exists, skipping...")
            
            # Commit all changes
            connection.commit()
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        return False

def verify_setup():
    """Verify the AWS RDS setup"""
    print_step("5", "Verifying Setup")
    
    try:
        connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            database=AWS_RDS_CONFIG["database"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        with connection.cursor() as cursor:
            # Get database info
            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()[0]
            
            # Get users count
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            # Get all users
            cursor.execute("SELECT id, email, nom, prenom, classe FROM users")
            users = cursor.fetchall()
            
            print(f"✅ Setup verification successful!")
            print(f"📊 Database: {current_db}")
            print(f"🌐 Host: {AWS_RDS_CONFIG['host']}")
            print(f"👥 Total users: {user_count}")
            
            print(f"\n👥 Users in database:")
            for user in users:
                print(f"   - {user[3]} {user[2]} ({user[1]}) - {user[4]}")
        
        connection.close()
        return True
        
    except Exception as e:
        print(f"❌ Setup verification failed: {e}")
        return False

def migrate_from_sqlite():
    """Migrate data from SQLite to AWS RDS"""
    print_step("6", "Migrating from SQLite (if exists)")
    
    sqlite_file = "m2dsia_local.db"
    
    if not os.path.exists(sqlite_file):
        print(f"⚠️  SQLite file '{sqlite_file}' not found, skipping migration")
        return True
    
    try:
        # Read from SQLite
        import sqlite3
        
        sqlite_conn = sqlite3.connect(sqlite_file)
        sqlite_cursor = sqlite_conn.cursor()
        
        # Get all users from SQLite
        sqlite_cursor.execute("SELECT email, nom, prenom, classe FROM users")
        sqlite_users = sqlite_cursor.fetchall()
        
        sqlite_conn.close()
        
        if not sqlite_users:
            print("⚠️  No users found in SQLite database")
            return True
            
        print(f"📊 Found {len(sqlite_users)} users in SQLite database")
        
        # Migrate to AWS RDS
        aws_connection = pymysql.connect(
            host=AWS_RDS_CONFIG["host"],
            user=AWS_RDS_CONFIG["user"],
            password=AWS_RDS_CONFIG["password"],
            database=AWS_RDS_CONFIG["database"],
            port=AWS_RDS_CONFIG["port"],
            connect_timeout=30
        )
        
        migrated_count = 0
        
        with aws_connection.cursor() as cursor:
            for email, nom, prenom, classe in sqlite_users:
                # Check if user already exists in AWS RDS
                cursor.execute("SELECT COUNT(*) FROM users WHERE email = %s", (email,))
                count = cursor.fetchone()[0]
                
                if count == 0:
                    cursor.execute(
                        "INSERT INTO users (email, nom, prenom, classe) VALUES (%s, %s, %s, %s)",
                        (email, nom, prenom, classe)
                    )
                    migrated_count += 1
                    print(f"✅ Migrated user: {email}")
                else:
                    print(f"⚠️  User {email} already exists in AWS RDS")
            
            # Commit all changes
            aws_connection.commit()
        
        aws_connection.close()
        print(f"✅ Migration completed! {migrated_count} users migrated to AWS RDS")
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def configure_environment():
    """Configure environment to use AWS RDS"""
    print_step("7", "Configuring Environment")
    
    try:
        # Create .env file
        env_content = f"""# Environment Configuration
USE_AWS_RDS=true
ENVIRONMENT=production

# AWS RDS Configuration
DB_HOST={AWS_RDS_CONFIG['host']}
DB_USER={AWS_RDS_CONFIG['user']}
DB_PASSWORD={AWS_RDS_CONFIG['password']}
DB_NAME={AWS_RDS_CONFIG['database']}
DB_PORT={AWS_RDS_CONFIG['port']}

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
"""
        
        with open(".env", "w") as f:
            f.write(env_content)
        
        print("✅ Environment configured for AWS RDS")
        print("📁 Created .env file with AWS RDS settings")
        return True
        
    except Exception as e:
        print(f"❌ Environment configuration failed: {e}")
        return False

def main():
    """Main setup function"""
    print_header("AWS RDS Database Setup - FIXED VERSION")
    print("🎯 Setting up M2DSIA application with AWS RDS MySQL")
    print(f"🌐 Target: {AWS_RDS_CONFIG['host']}")
    print(f"🗄️  Database: {AWS_RDS_CONFIG['database']}")
    
    # Setup steps
    steps = [
        ("Test Connection", test_connection),
        ("Create Database", create_database),
        ("Create Tables", create_tables),
        ("Add Sample Data", add_sample_data),
        ("Verify Setup", verify_setup),
        ("Migrate from SQLite", migrate_from_sqlite),
        ("Configure Environment", configure_environment)
    ]
    
    failed_steps = []
    
    for step_name, step_func in steps:
        try:
            if not step_func():
                failed_steps.append(step_name)
        except Exception as e:
            print(f"❌ Step '{step_name}' failed with exception: {e}")
            failed_steps.append(step_name)
    
    # Summary
    print_header("SETUP SUMMARY")
    
    if not failed_steps:
        print("🎉 AWS RDS SETUP COMPLETED SUCCESSFULLY!")
        print("\n🚀 Next steps:")
        print("1. Update db/connexion.py with the corrected version")
        print("2. Run: python api/main.py")
        print("3. Test: http://localhost:8000/docs")
        print("4. Check users: http://localhost:8000/users/")
        print("\n📊 Your app is now using AWS RDS MySQL!")
        
    else:
        print(f"❌ Setup completed with {len(failed_steps)} failed steps:")
        for step in failed_steps:
            print(f"   - {step}")
        
        print("\n🔧 Troubleshooting:")
        print("1. Check the hostname in db/connexion.py")
        print("2. Verify AWS RDS instance is running")
        print("3. Check security groups and network settings")

if __name__ == "__main__":
    main()