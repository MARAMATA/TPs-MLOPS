# quick_aws_test.py 
import socket
import pymysql
import time

# Configuration AWS RDS - HOSTNAME CORRIGÉ
HOST = "m2dsia-mlops.cfuik82swe2y.eu-central-1.rds.amazonaws.com"  # CORRIGÉ !
USER = "root"
PASSWORD = "rootM2dsia"
DATABASE = "m2dsia_maramata"
PORT = 3306

def test_aws_connection():
    """Test rapide de connexion AWS RDS"""
    print("🔍 Test Rapide de Connexion AWS RDS - VERSION CORRIGÉE")
    print("=" * 60)
    print(f"🎯 Hostname: {HOST}")
    
    # Test 1: DNS Resolution
    print("\n1. Test DNS Resolution...")
    try:
        ip = socket.gethostbyname(HOST)
        print(f"✅ DNS OK: {HOST} -> {ip}")
    except Exception as e:
        print(f"❌ DNS FAILED: {e}")
        return False
    
    # Test 2: Port Connectivity
    print("\n2. Test Port Connectivity...")
    try:
        sock = socket.create_connection((HOST, PORT), timeout=10)
        sock.close()
        print(f"✅ Port OK: {HOST}:{PORT}")
    except Exception as e:
        print(f"❌ Port FAILED: {e}")
        return False
    
    # Test 3: MySQL Connection
    print("\n3. Test MySQL Connection...")
    try:
        conn = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            port=PORT,
            connect_timeout=30
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"✅ MySQL OK: {version[0]}")
            
        conn.close()
        print(f"✅ Credentials OK: {USER}@{HOST}")
        
    except Exception as e:
        print(f"❌ MySQL FAILED: {e}")
        return False
    
    # Test 4: Database Access
    print("\n4. Test Database Access...")
    try:
        conn = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            connect_timeout=30
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SELECT DATABASE()")
            db = cursor.fetchone()
            print(f"✅ Database OK: {db[0]}")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Database FAILED: {e}")
        print("💡 Database might not exist - will be created automatically")
    
    # Test 5: Show Tables
    print("\n5. Test Show Tables...")
    try:
        conn = pymysql.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=PORT,
            connect_timeout=30
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            if tables:
                print(f"✅ Tables found: {len(tables)}")
                for table in tables:
                    print(f"   📋 {table[0]}")
            else:
                print("⚠️  No tables found - will be created automatically")
            
        conn.close()
        
    except Exception as e:
        print(f"❌ Show Tables FAILED: {e}")
    
    print("\n🎉 AWS RDS Connection Test PASSED!")
    print("🚀 You can now run: python setup_aws_database.py")
    print(f"🌐 Connected to: {HOST}")
    print(f"📊 Database: {DATABASE}")
    return True

if __name__ == "__main__":
    test_aws_connection()