"""
Database Connection Manager
"""
import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
from contextlib import contextmanager

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME', 'workshop_management'),
    'user': os.getenv('DB_USER', 'root'),
    'password': os.getenv('DB_PASSWORD', ''),
    'autocommit': False,  # We'll handle transactions manually
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_unicode_ci'
}


def get_db_connection():
    """
    Create and return a database connection
    
    Returns:
        mysql.connector.connection.MySQLConnection: Database connection
        
    Raises:
        Error: If connection fails
    """
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        raise


def close_db_connection(connection):
    """
    Close a database connection
    
    Args:
        connection: MySQL connection to close
    """
    if connection and connection.is_connected():
        connection.close()


@contextmanager
def get_db_cursor(commit=True):
    """
    Context manager for database operations
    
    Usage:
        with get_db_cursor() as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
    
    Args:
        commit: Whether to commit the transaction (default: True)
        
    Yields:
        mysql.connector.cursor.MySQLCursor: Database cursor
    """
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)  # Return results as dictionaries
    
    try:
        yield cursor
        if commit:
            connection.commit()
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        close_db_connection(connection)


def init_db():
    """
    Initialize database schema
    Creates all tables if they don't exist
    """
    connection = get_db_connection()
    cursor = connection.cursor()
    
    try:
        # Create users table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id VARCHAR(36) PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                INDEX idx_email (email)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create workshops table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS workshops (
                id VARCHAR(36) PRIMARY KEY,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                status ENUM('pending', 'ongoing', 'completed') DEFAULT 'pending',
                signup_enabled BOOLEAN DEFAULT TRUE,
                owner_id VARCHAR(36),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_owner (owner_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create participants table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS participants (
                id VARCHAR(36) PRIMARY KEY,
                workshop_id VARCHAR(36) NOT NULL,
                user_id VARCHAR(36) NOT NULL,
                status ENUM('pending', 'joined', 'rejected', 'waitlisted') DEFAULT 'pending',
                requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                approved_at TIMESTAMP NULL,
                approved_by VARCHAR(36),
                FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (approved_by) REFERENCES users(id) ON DELETE SET NULL,
                UNIQUE KEY unique_workshop_user (workshop_id, user_id),
                INDEX idx_workshop (workshop_id),
                INDEX idx_user (user_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create challenges table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenges (
                id VARCHAR(36) PRIMARY KEY,
                workshop_id VARCHAR(36) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                html_content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
                INDEX idx_workshop (workshop_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        connection.commit()
        print("Database schema initialized successfully")
        
    except Error as e:
        connection.rollback()
        print(f"Error initializing database: {e}")
        raise
    finally:
        cursor.close()
        close_db_connection(connection)


def test_connection():
    """
    Test database connection
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        connection = get_db_connection()
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Successfully connected to MySQL Server version {db_info}")
            close_db_connection(connection)
            return True
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        return False
