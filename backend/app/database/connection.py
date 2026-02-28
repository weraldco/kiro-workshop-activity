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
                workshop_date DATE NULL,
                venue_type ENUM('online', 'physical') DEFAULT 'online',
                venue_address TEXT NULL,
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
                order_index INT DEFAULT 0,
                points INT DEFAULT 20,
                solution TEXT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
                INDEX idx_workshop (workshop_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create lessons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lessons (
                id VARCHAR(36) PRIMARY KEY,
                workshop_id VARCHAR(36) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                content TEXT,
                order_index INT DEFAULT 0,
                points INT DEFAULT 10,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
                INDEX idx_workshop (workshop_id),
                INDEX idx_order (order_index)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create lesson_materials table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS lesson_materials (
                id VARCHAR(36) PRIMARY KEY,
                lesson_id VARCHAR(36) NOT NULL,
                material_type ENUM('video', 'pdf', 'link') NOT NULL,
                title VARCHAR(200) NOT NULL,
                url TEXT NOT NULL,
                file_size BIGINT NULL,
                duration INT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
                INDEX idx_lesson (lesson_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create exams table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exams (
                id VARCHAR(36) PRIMARY KEY,
                workshop_id VARCHAR(36) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                duration_minutes INT DEFAULT 60,
                passing_score INT DEFAULT 70,
                points INT DEFAULT 50,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (workshop_id) REFERENCES workshops(id) ON DELETE CASCADE,
                INDEX idx_workshop (workshop_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create exam_questions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_questions (
                id VARCHAR(36) PRIMARY KEY,
                exam_id VARCHAR(36) NOT NULL,
                question_text TEXT NOT NULL,
                question_type ENUM('multiple_choice', 'true_false', 'short_answer') DEFAULT 'multiple_choice',
                options JSON NULL,
                correct_answer TEXT NOT NULL,
                points INT DEFAULT 10,
                order_index INT DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                INDEX idx_exam (exam_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create user_progress table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_progress (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                lesson_id VARCHAR(36) NOT NULL,
                completed BOOLEAN DEFAULT FALSE,
                completed_at TIMESTAMP NULL,
                points_earned INT DEFAULT 0,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (lesson_id) REFERENCES lessons(id) ON DELETE CASCADE,
                UNIQUE KEY unique_user_lesson (user_id, lesson_id),
                INDEX idx_user (user_id),
                INDEX idx_lesson (lesson_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create challenge_submissions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS challenge_submissions (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                challenge_id VARCHAR(36) NOT NULL,
                submission_text TEXT,
                submission_url TEXT NULL,
                status ENUM('pending', 'passed', 'failed') DEFAULT 'pending',
                points_earned INT DEFAULT 0,
                submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                reviewed_at TIMESTAMP NULL,
                reviewed_by VARCHAR(36) NULL,
                feedback TEXT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (challenge_id) REFERENCES challenges(id) ON DELETE CASCADE,
                FOREIGN KEY (reviewed_by) REFERENCES users(id) ON DELETE SET NULL,
                INDEX idx_user (user_id),
                INDEX idx_challenge (challenge_id),
                INDEX idx_status (status)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create exam_attempts table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS exam_attempts (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                exam_id VARCHAR(36) NOT NULL,
                answers JSON NOT NULL,
                score INT DEFAULT 0,
                points_earned INT DEFAULT 0,
                passed BOOLEAN DEFAULT FALSE,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                submitted_at TIMESTAMP NULL,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (exam_id) REFERENCES exams(id) ON DELETE CASCADE,
                INDEX idx_user (user_id),
                INDEX idx_exam (exam_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create user_points table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_points (
                user_id VARCHAR(36) PRIMARY KEY,
                total_points INT DEFAULT 0,
                lessons_completed INT DEFAULT 0,
                challenges_completed INT DEFAULT 0,
                exams_passed INT DEFAULT 0,
                current_rank INT DEFAULT 0,
                previous_rank INT DEFAULT 0,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_total_points (total_points DESC),
                INDEX idx_rank (current_rank)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci
        """)
        
        # Create leaderboard_history table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS leaderboard_history (
                id VARCHAR(36) PRIMARY KEY,
                user_id VARCHAR(36) NOT NULL,
                rank_position INT NOT NULL,
                total_points INT NOT NULL,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                INDEX idx_user (user_id),
                INDEX idx_recorded (recorded_at)
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
