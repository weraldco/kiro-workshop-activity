"""
Database Migration Script

Applies the learning features migration to the database.

Usage:
    python migrate_db.py
"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import get_db_connection, close_db_connection


def run_migration():
    """Run the migration SQL file"""
    print("=" * 60)
    print("Workshop Management System - Database Migration")
    print("=" * 60)
    print()
    
    migration_file = os.path.join(
        os.path.dirname(__file__),
        'migrations',
        'add_learning_features.sql'
    )
    
    if not os.path.exists(migration_file):
        print(f"❌ Migration file not found: {migration_file}")
        return 1
    
    print(f"Reading migration file: {migration_file}")
    
    with open(migration_file, 'r') as f:
        sql_content = f.read()
    
    # Remove comments and split by semicolon
    lines = sql_content.split('\n')
    cleaned_lines = []
    for line in lines:
        # Remove comments
        if line.strip().startswith('--'):
            continue
        cleaned_lines.append(line)
    
    cleaned_sql = '\n'.join(cleaned_lines)
    
    # Split by semicolon and filter out empty statements
    statements = [s.strip() for s in cleaned_sql.split(';') if s.strip()]
    
    print(f"Found {len(statements)} SQL statements to execute\n")
    
    connection = None
    try:
        connection = get_db_connection()
        cursor = connection.cursor()
        
        for i, statement in enumerate(statements, 1):
            print(f"[{i}/{len(statements)}] Executing statement...")
            try:
                cursor.execute(statement)
                connection.commit()
                print(f"✅ Success")
            except Exception as e:
                # Check if it's a "column already exists" or "table already exists" error
                if 'Duplicate column' in str(e) or 'already exists' in str(e):
                    print(f"⚠️  Already applied: {str(e)}")
                else:
                    print(f"❌ Error: {e}")
                    connection.rollback()
                    raise
        
        print("\n" + "=" * 60)
        print("✅ Migration completed successfully!")
        print("=" * 60)
        print("\nNew tables created:")
        print("  - lessons")
        print("  - lesson_materials")
        print("  - exams")
        print("  - exam_questions")
        print("  - user_progress")
        print("  - challenge_submissions")
        print("  - exam_attempts")
        print("  - user_points")
        print("  - leaderboard_history")
        print("\nWorkshops table updated with:")
        print("  - workshop_date")
        print("  - venue_type")
        print("  - venue_address")
        print("\nChallenges table updated with:")
        print("  - order_index")
        print("  - points")
        print("  - solution")
        
        cursor.close()
        return 0
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        return 1
    finally:
        if connection:
            close_db_connection(connection)


if __name__ == '__main__':
    sys.exit(run_migration())
