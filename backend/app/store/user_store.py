"""
User Store - MySQL Implementation
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.connection import get_db_cursor
from mysql.connector import Error, IntegrityError


class UserStore:
    """Manages user data persistence using MySQL"""
    
    def __init__(self, file_path: str = None):
        """
        Initialize UserStore
        
        Args:
            file_path: Ignored (for compatibility with JSON version)
        """
        # file_path is ignored - we use MySQL connection from environment
        pass
    
    def create_user(self, email: str, password_hash: str, name: str) -> Dict[str, Any]:
        """
        Create a new user
        
        Args:
            email: User email (unique)
            password_hash: Bcrypt hashed password
            name: User's full name
            
        Returns:
            Created user dict (without password_hash)
            
        Raises:
            ValueError: If email already exists
        """
        user_id = str(uuid.uuid4())
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (id, email, password_hash, name)
                    VALUES (%s, %s, %s, %s)
                """, (user_id, email, password_hash, name))
                
                # Fetch the created user
                cursor.execute("""
                    SELECT id, email, name, created_at, updated_at
                    FROM users
                    WHERE id = %s
                """, (user_id,))
                
                user = cursor.fetchone()
                return self._format_user(user)
                
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                raise ValueError(f"User with email {email} already exists")
            raise
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email (includes password_hash for authentication)
        
        Args:
            email: User email
            
        Returns:
            User dict with password_hash, or None if not found
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT id, email, password_hash, name, created_at, updated_at
                FROM users
                WHERE email = %s
            """, (email,))
            
            user = cursor.fetchone()
            return self._format_user(user, include_password=True) if user else None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID (without password_hash)
        
        Args:
            user_id: User ID
            
        Returns:
            User dict without password_hash, or None if not found
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT id, email, name, created_at, updated_at
                FROM users
                WHERE id = %s
            """, (user_id,))
            
            user = cursor.fetchone()
            return self._format_user(user) if user else None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users (without password_hash)
        
        Returns:
            List of user dicts without password_hash
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT id, email, name, created_at, updated_at
                FROM users
                ORDER BY created_at DESC
            """)
            
            users = cursor.fetchall()
            return [self._format_user(u) for u in users]
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user fields
        
        Args:
            user_id: User ID
            updates: Dict of fields to update (name, email, password_hash)
            
        Returns:
            Updated user dict without password_hash, or None if not found
        """
        # Build dynamic UPDATE query
        update_fields = []
        values = []
        
        if 'name' in updates:
            update_fields.append("name = %s")
            values.append(updates['name'])
        
        if 'email' in updates:
            update_fields.append("email = %s")
            values.append(updates['email'])
        
        if 'password_hash' in updates:
            update_fields.append("password_hash = %s")
            values.append(updates['password_hash'])
        
        if not update_fields:
            return self.get_user_by_id(user_id)
        
        values.append(user_id)
        
        try:
            with get_db_cursor() as cursor:
                query = f"""
                    UPDATE users
                    SET {', '.join(update_fields)}
                    WHERE id = %s
                """
                cursor.execute(query, values)
                
                if cursor.rowcount == 0:
                    return None
                
                # Fetch updated user within same transaction
                cursor.execute("""
                    SELECT id, email, name, created_at, updated_at
                    FROM users
                    WHERE id = %s
                """, (user_id,))
                
                user = cursor.fetchone()
                return self._format_user(user)
                
        except IntegrityError as e:
            if 'Duplicate entry' in str(e):
                raise ValueError(f"Email {updates.get('email')} already in use")
            raise
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False if not found
        """
        with get_db_cursor() as cursor:
            cursor.execute("""
                DELETE FROM users
                WHERE id = %s
            """, (user_id,))
            
            return cursor.rowcount > 0
    
    def _format_user(self, user: Optional[Dict[str, Any]], include_password: bool = False) -> Optional[Dict[str, Any]]:
        """
        Format user dict from database result
        
        Args:
            user: User dict from database
            include_password: Whether to include password_hash
            
        Returns:
            Formatted user dict
        """
        if not user:
            return None
        
        formatted = {
            'id': user['id'],
            'email': user['email'],
            'name': user['name'],
            'created_at': user['created_at'].isoformat() if user.get('created_at') else None,
            'updated_at': user['updated_at'].isoformat() if user.get('updated_at') else None
        }
        
        if include_password and 'password_hash' in user:
            formatted['password_hash'] = user['password_hash']
        
        return formatted
