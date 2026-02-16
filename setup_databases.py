"""
Setup script to create databases if they don't exist
"""
import pymysql
from pymongo import MongoClient
from config import (
    MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWORD, MYSQL_DATABASE,
    MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
)

def setup_mysql():
    """Create MySQL database if it doesn't exist"""
    try:
        # Connect without specifying database
        connection = pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            charset='utf8mb4'
        )
        
        with connection.cursor() as cursor:
            # Create database if it doesn't exist
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_DATABASE} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"[OK] MySQL database '{MYSQL_DATABASE}' created/verified successfully")
        
        connection.close()
        return True
    except pymysql.Error as e:
        print(f"[X] Error setting up MySQL database: {e}")
        print(f"  Make sure MySQL is running and credentials in .env are correct")
        return False

def setup_mongodb():
    """Verify MongoDB connection and create database if needed"""
    try:
        client = MongoClient(
            host=MONGODB_HOST,
            port=MONGODB_PORT,
            serverSelectionTimeoutMS=5000
        )
        # Test connection
        client.admin.command('ping')
        # Access the database (creates it if it doesn't exist)
        db = client[MONGODB_DATABASE]
        # Create a dummy collection to ensure database exists
        db['_setup_check'].insert_one({'check': True})
        db['_setup_check'].drop()
        print(f"[OK] MongoDB database '{MONGODB_DATABASE}' created/verified successfully")
        client.close()
        return True
    except Exception as e:
        print(f"[X] Error setting up MongoDB database: {e}")
        print(f"  Make sure MongoDB is running and accessible")
        return False

if __name__ == '__main__':
    print("=== Database Setup ===")
    print("\nSetting up MySQL...")
    mysql_ok = setup_mysql()
    
    print("\nSetting up MongoDB...")
    mongodb_ok = setup_mongodb()
    
    print("\n=== Setup Summary ===")
    if mysql_ok and mongodb_ok:
        print("[OK] All databases are ready!")
        print("\nYou can now run:")
        print("  python seed_data.py  # To add sample data")
        print("  python app.py        # To start the application")
    else:
        print("[X] Some databases failed to set up. Please check the errors above.")
