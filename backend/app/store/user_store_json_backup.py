"""
User Store - User data persistence layer
"""
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from app.store.file_lock import FileLock


class UserStore:
    """Manages user data persistence"""
    
    def __init__(self, file_path: str):
        """
        Initialize UserStore
        
        Args:
            file_path: Path to JSON data file
        """
        self.file_path = file_path
    
    def _read_data(self) -> Dict[str, Any]:
        """Read data from JSON file"""
        import json
        
        with FileLock(self.file_path):
            try:
                with open(self.file_path, 'r') as f:
                    return json.load(f)
            except FileNotFoundError:
                return {"users": [], "workshops": [], "participants": [], "challenges": []}
            except json.JSONDecodeError:
                return {"users": [], "workshops": [], "participants": [], "challenges": []}
    
    def _write_data(self, data: Dict[str, Any]) -> None:
        """Write data to JSON file"""
        import json
        
        with FileLock(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
    
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
        data = self._read_data()
        
        # Check for duplicate email
        if any(u['email'] == email for u in data.get('users', [])):
            raise ValueError(f"User with email {email} already exists")
        
        # Create user
        now = datetime.now(timezone.utc).isoformat()
        user = {
            "id": str(uuid.uuid4()),
            "email": email,
            "password_hash": password_hash,
            "name": name,
            "created_at": now,
            "updated_at": now
        }
        
        # Add to data
        if 'users' not in data:
            data['users'] = []
        data['users'].append(user)
        
        # Save
        self._write_data(data)
        
        # Return user without password_hash
        return self._sanitize_user(user)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Get user by email (includes password_hash for authentication)
        
        Args:
            email: User email
            
        Returns:
            User dict with password_hash, or None if not found
        """
        data = self._read_data()
        
        for user in data.get('users', []):
            if user['email'] == email:
                return user
        
        return None
    
    def get_user_by_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user by ID (without password_hash)
        
        Args:
            user_id: User ID
            
        Returns:
            User dict without password_hash, or None if not found
        """
        data = self._read_data()
        
        for user in data.get('users', []):
            if user['id'] == user_id:
                return self._sanitize_user(user)
        
        return None
    
    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Get all users (without password_hash)
        
        Returns:
            List of user dicts without password_hash
        """
        data = self._read_data()
        return [self._sanitize_user(u) for u in data.get('users', [])]
    
    def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update user fields
        
        Args:
            user_id: User ID
            updates: Dict of fields to update (name, email, password_hash)
            
        Returns:
            Updated user dict without password_hash, or None if not found
        """
        data = self._read_data()
        
        for i, user in enumerate(data.get('users', [])):
            if user['id'] == user_id:
                # Update allowed fields
                if 'name' in updates:
                    user['name'] = updates['name']
                if 'email' in updates:
                    # Check for duplicate email
                    if any(u['email'] == updates['email'] and u['id'] != user_id 
                           for u in data['users']):
                        raise ValueError(f"Email {updates['email']} already in use")
                    user['email'] = updates['email']
                if 'password_hash' in updates:
                    user['password_hash'] = updates['password_hash']
                
                user['updated_at'] = datetime.now(timezone.utc).isoformat()
                
                data['users'][i] = user
                self._write_data(data)
                
                return self._sanitize_user(user)
        
        return None
    
    def delete_user(self, user_id: str) -> bool:
        """
        Delete a user
        
        Args:
            user_id: User ID
            
        Returns:
            True if deleted, False if not found
        """
        data = self._read_data()
        
        original_count = len(data.get('users', []))
        data['users'] = [u for u in data.get('users', []) if u['id'] != user_id]
        
        if len(data['users']) < original_count:
            self._write_data(data)
            return True
        
        return False
    
    def _sanitize_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove password_hash from user dict
        
        Args:
            user: User dict with password_hash
            
        Returns:
            User dict without password_hash
        """
        sanitized = user.copy()
        sanitized.pop('password_hash', None)
        return sanitized
