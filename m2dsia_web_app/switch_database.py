# switch_database.py - Script pour basculer entre SQLite et AWS RDS
import os
import sys
import argparse

def create_env_file(use_aws=True):
    """Create .env file with database configuration"""
    
    if use_aws:
        env_content = """# Environment Configuration - AWS RDS
USE_AWS_RDS=true
ENVIRONMENT=production

# AWS RDS Configuration
DB_HOST=m2-dsia.cfuik82swe2y.eu-central-1.rds.amazonaws.com
DB_USER=root
DB_PASSWORD=rootM2dsia
DB_NAME=m2dsia_maramata
DB_PORT=3306

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
"""
    else:
        env_content = """# Environment Configuration - SQLite Local
USE_AWS_RDS=false
ENVIRONMENT=development

# Local SQLite Configuration
DB_FILE=m2dsia_local.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
"""
    
    with open(".env", "w") as f:
        f.write(env_content)
    
    db_type = "AWS RDS" if use_aws else "SQLite Local"
    print(f"✅ Environment configured for {db_type}")
    print(f"📁 Updated .env file")

def test_current_connection():
    """Test current database connection"""
    try:
        sys.path.append(os.path.abspath(os.path.dirname(__file__)))
        
        from db.connexion import test_connection, get_current_database_info
        
        print("🔍 Testing current database connection...")
        
        if test_connection():
            info = get_current_database_info()
            print(f"✅ Connection successful!")
            print(f"📊 Database info: {info}")
            return True
        else:
            print("❌ Connection failed!")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def show_current_status():
    """Show current database configuration"""
    print("📊 Current Database Status")
    print("=" * 50)
    
    # Check .env file
    if os.path.exists(".env"):
        print("📁 .env file exists")
        with open(".env", "r") as f:
            content = f.read()
            if "USE_AWS_RDS=true" in content:
                print("🌐 Configured for: AWS RDS")
            else:
                print("💾 Configured for: SQLite Local")
    else:
        print("⚠️  No .env file found")
    
    # Check database files
    if os.path.exists("m2dsia_local.db"):
        print("📄 SQLite database file exists")
    else:
        print("📄 No SQLite database file found")
    
    # Test connection
    test_current_connection()

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Switch between SQLite and AWS RDS databases")
    parser.add_argument("--database", "-d", choices=["sqlite", "aws"], 
                       help="Choose database: sqlite or aws")
    parser.add_argument("--status", "-s", action="store_true", 
                       help="Show current database status")
    parser.add_argument("--test", "-t", action="store_true", 
                       help="Test current database connection")
    
    args = parser.parse_args()
    
    if args.status:
        show_current_status()
        return
    
    if args.test:
        test_current_connection()
        return
    
    if args.database:
        if args.database == "sqlite":
            print("🔄 Switching to SQLite Local Database...")
            create_env_file(use_aws=False)
            
            # Set environment variable for immediate effect
            os.environ["USE_AWS_RDS"] = "false"
            
            print("\n🚀 Next steps:")
            print("1. Run: python setup_local_database.py")
            print("2. Run: python api/main.py")
            print("3. Test: http://localhost:8000/docs")
            
        elif args.database == "aws":
            print("🔄 Switching to AWS RDS Database...")
            create_env_file(use_aws=True)
            
            # Set environment variable for immediate effect
            os.environ["USE_AWS_RDS"] = "true"
            
            print("\n🚀 Next steps:")
            print("1. Run: python diagnose_aws_connection.py (optional)")
            print("2. Run: python setup_aws_database.py")
            print("3. Run: python api/main.py")
            print("4. Test: http://localhost:8000/docs")
            
        print(f"\n✅ Database switched to {args.database.upper()}")
        print("🔄 Restart your API server to apply changes")
        
    else:
        print("🔧 M2DSIA Database Switcher")
        print("=" * 40)
        print("Usage:")
        print("  python switch_database.py --database sqlite  # Switch to SQLite")
        print("  python switch_database.py --database aws     # Switch to AWS RDS")
        print("  python switch_database.py --status           # Show current status")
        print("  python switch_database.py --test             # Test connection")

if __name__ == "__main__":
    main()