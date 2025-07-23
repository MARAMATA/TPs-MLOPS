# tests/main.py
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from schemas.schemas import UserCreate
from db.connexion import SessionLocal
from db.crud import create_user, get_user_by_email, get_all_users, update_user, delete_user
from db.crud import get_users_by_class, get_active_users, deactivate_user
from schemas.schemas import UserUpdate

def test_create_user():
    """Test creating a new user"""
    print("🧪 Testing user creation...")
    
    db = SessionLocal()
    
    # Test data
    test_data = {
        "email": "test.user@isi.com",
        "nom": "Test",
        "prenom": "User",
        "classe": "MLOps 2025"
    }
    
    try:
        # Create user
        user = UserCreate(**test_data)
        result = create_user(db, user)
        
        print(f"✓ User created successfully: {result.prenom} {result.nom} ({result.email})")
        return True
    except Exception as e:
        print(f"✗ Error creating user: {e}")
        return False
    finally:
        db.close()

def test_get_user():
    """Test getting a user by email"""
    print("🧪 Testing user retrieval...")
    
    db = SessionLocal()
    
    try:
        # Get user by email
        user = get_user_by_email(db, "test.user@isi.com")
        
        if user:
            print(f"✓ User found: {user.prenom} {user.nom} ({user.email})")
            return True
        else:
            print("✗ User not found")
            return False
    except Exception as e:
        print(f"✗ Error getting user: {e}")
        return False
    finally:
        db.close()

def test_get_all_users():
    """Test getting all users"""
    print("🧪 Testing get all users...")
    
    db = SessionLocal()
    
    try:
        users = get_all_users(db)
        print(f"✓ Found {len(users)} users in database:")
        
        for user in users:
            print(f"  - {user.prenom} {user.nom} ({user.email}) - {user.classe}")
        
        return True
    except Exception as e:
        print(f"✗ Error getting all users: {e}")
        return False
    finally:
        db.close()

def test_update_user():
    """Test updating a user"""
    print("🧪 Testing user update...")
    
    db = SessionLocal()
    
    try:
        # Find user to update
        user = get_user_by_email(db, "test.user@isi.com")
        if not user:
            print("✗ Test user not found for update")
            return False
        
        # Update user
        update_data = UserUpdate(classe="MLOps 2026", nom="Updated Test")
        updated_user = update_user(db, user.id, update_data)
        
        if updated_user:
            print(f"✓ User updated successfully: {updated_user.nom} - {updated_user.classe}")
            return True
        else:
            print("✗ User update failed")
            return False
    except Exception as e:
        print(f"✗ Error updating user: {e}")
        return False
    finally:
        db.close()

def test_get_users_by_class():
    """Test getting users by class"""
    print("🧪 Testing get users by class...")
    
    db = SessionLocal()
    
    try:
        users = get_users_by_class(db, "MLOps 2025")
        print(f"✓ Found {len(users)} users in MLOps 2025 class")
        
        for user in users:
            print(f"  - {user.prenom} {user.nom} ({user.email})")
        
        return True
    except Exception as e:
        print(f"✗ Error getting users by class: {e}")
        return False
    finally:
        db.close()

def test_deactivate_user():
    """Test deactivating a user"""
    print("🧪 Testing user deactivation...")
    
    db = SessionLocal()
    
    try:
        # Find user to deactivate
        user = get_user_by_email(db, "test.user@isi.com")
        if not user:
            print("✗ Test user not found for deactivation")
            return False
        
        # Deactivate user
        deactivated_user = deactivate_user(db, user.id)
        
        if deactivated_user and not deactivated_user.is_active:
            print(f"✓ User deactivated successfully: {deactivated_user.email}")
            return True
        else:
            print("✗ User deactivation failed")
            return False
    except Exception as e:
        print(f"✗ Error deactivating user: {e}")
        return False
    finally:
        db.close()

def test_get_active_users():
    """Test getting only active users"""
    print("🧪 Testing get active users...")
    
    db = SessionLocal()
    
    try:
        active_users = get_active_users(db)
        all_users = get_all_users(db)
        
        print(f"✓ Found {len(active_users)} active users out of {len(all_users)} total users")
        
        for user in active_users:
            print(f"  - {user.prenom} {user.nom} ({user.email}) - Active: {user.is_active}")
        
        return True
    except Exception as e:
        print(f"✗ Error getting active users: {e}")
        return False
    finally:
        db.close()

def cleanup_test_data():
    """Clean up test data"""
    print("🧹 Cleaning up test data...")
    
    db = SessionLocal()
    
    try:
        # Find and delete test user
        user = get_user_by_email(db, "test.user@isi.com")
        if user:
            success = delete_user(db, user.id)
            if success:
                print("✓ Test user deleted successfully")
            else:
                print("✗ Failed to delete test user")
        else:
            print("- No test user found to delete")
    except Exception as e:
        print(f"✗ Error cleaning up test data: {e}")
    finally:
        db.close()

def main():
    """Run all tests"""
    print("🚀 Running M2DSIA Database Tests")
    print("=" * 50)
    
    tests = [
        test_create_user,
        test_get_user,
        test_get_all_users,
        test_update_user,
        test_get_users_by_class,
        test_deactivate_user,
        test_get_active_users,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"✗ Test {test.__name__} failed with exception: {e}")
            failed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    # Cleanup
    cleanup_test_data()
    
    if failed == 0:
        print("🎉 All tests passed!")
    else:
        print(f"❌ {failed} tests failed!")

if __name__ == "__main__":
    main()