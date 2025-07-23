# setup_local_database.py 
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from db.connexion import Base, engine, SessionLocal
from models.models import User as UserModel
from schemas.schemas import UserCreate
from db.crud import create_user, get_all_users

def create_tables():
    """
    Create all tables defined in models
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def add_sample_data():
    """
    Add sample data to test the setup
    """
    try:
        db = SessionLocal()
        
        # Sample users data
        sample_users = [
            {
                "email": "john.doe@isi.com",
                "nom": "Doe",
                "prenom": "John",
                "classe": "MLOps 2025"
            },
            {
                "email": "jane.smith@isi.com",
                "nom": "Smith",
                "prenom": "Jane",
                "classe": "MLOps 2025"
            },
            {
                "email": "lipson.soume@isi.com",
                "nom": "Soume",
                "prenom": "Lipson",
                "classe": "MLOps 2025"
            },
            {
                "email": "maramata.student@isi.com",
                "nom": "Maramata",
                "prenom": "Student",
                "classe": "MLOps 2025"
            }
        ]
        
        # Add users if they don't exist
        for user_data in sample_users:
            user = UserCreate(**user_data)
            
            # Check if user already exists
            existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
            if not existing_user:
                create_user(db, user)
                print(f"✅ User {user.email} added successfully!")
            else:
                print(f"⚠️  User {user.email} already exists, skipping...")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        return False

def verify_setup():
    """
    Verify the database setup by querying all users
    """
    try:
        db = SessionLocal()
        users = get_all_users(db)
        
        print(f"\n✅ Database setup verification:")
        print(f"📊 Total users in database: {len(users)}")
        
        for user in users:
            print(f"👤 {user.prenom} {user.nom} ({user.email}) - {user.classe}")
        
        db.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
        return False

def test_api_connection():
    """
    Test database connection through API
    """
    try:
        from db.connexion import test_connection
        return test_connection()
    except Exception as e:
        print(f"❌ Error testing API connection: {e}")
        return False

def main():
    """
    Main setup function
    """
    print("🚀 M2DSIA Database Setup (LOCAL SQLITE)")
    print("=" * 60)
    
    # Step 1: Test connection
    print("\n1. Testing database connection...")
    if not test_api_connection():
        print("Database connection test failed, but continuing with SQLite...")
    
    # Step 2: Create tables
    print("\n2. Creating tables...")
    if not create_tables():
        print("Failed to create tables. Exiting.")
        return
    
    # Step 3: Add sample data
    print("\n3. Adding sample data...")
    if not add_sample_data():
        print("Failed to add sample data.")
    
    # Step 4: Verify setup
    print("\n4. Verifying setup...")
    if verify_setup():
        print(f"\n🎉 LOCAL DATABASE SETUP COMPLETED SUCCESSFULLY!")
        print(f"📁 Database file: m2dsia_local.db")
        print(f"\n🚀 You can now:")
        print("- Run the API: python api/main.py")
        print("- Test endpoints at: http://localhost:8000/docs")
        print("- View all users at: http://localhost:8000/users/")
    else:
        print("\n❌ Database setup verification failed!")

if __name__ == "__main__":
    main()