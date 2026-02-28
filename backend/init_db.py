"""
Database Initialization Script

This script initializes the MySQL database schema.
Run this before starting the application for the first time.

Usage:
    python init_db.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import init_db, test_connection


def main():
    """Initialize the database"""
    print("=" * 60)
    print("Workshop Management System - Database Initialization")
    print("=" * 60)
    print()
    
    # Test connection first
    print("Testing database connection...")
    if not test_connection():
        print("\n❌ Failed to connect to database.")
        print("\nPlease check:")
        print("1. MySQL server is running")
        print("2. Database credentials in .env file are correct")
        print("3. Database 'workshop_management' exists")
        print("\nTo create the database, run:")
        print("   mysql -u root -p")
        print("   CREATE DATABASE workshop_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        return 1
    
    print("✅ Database connection successful\n")
    
    # Initialize schema
    print("Initializing database schema...")
    try:
        init_db()
        print("\n✅ Database schema initialized successfully!")
        print("\nTables created:")
        print("  - users")
        print("  - workshops")
        print("  - participants")
        print("  - challenges")
        print("\nYou can now start the application.")
        return 0
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
