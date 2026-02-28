"""
Workshop Store - MySQL Implementation
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.connection import get_db_cursor
from mysql.connector import Error


class WorkshopStore:
    """Manages workshop data persistence using MySQL"""
    
    def __init__(self):
        """Initialize WorkshopStore"""
        pass
    
    def create_workshop(self, title: str, description: str, owner_id: str,
                       workshop_date: str = None, venue_type: str = 'online',
                       venue_address: str = None) -> Dict[str, Any]:
        """
        Create a new workshop
        
        Args:
            title: Workshop title
            description: Workshop description
            owner_id: ID of the user creating the workshop
            workshop_date: Workshop date (YYYY-MM-DD format)
            venue_type: 'online' or 'physical'
            venue_address: Physical address if venue_type is 'physical'
            
        Returns:
            Created workshop dict
        """
        workshop_id = str(uuid.uuid4())
        
        with get_db_cursor() as cursor:
            cursor.execute("""
                INSERT INTO workshops (id, title, description, workshop_date, venue_type, 
                                     venue_address, status, signup_enabled, owner_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (workshop_id, title, description, workshop_date, venue_type, 
                  venue_address, 'pending', True, owner_id))
            
            # Fetch the created workshop
            cursor.execute("""
                SELECT id, title, description, workshop_date, venue_type, venue_address,
                       status, signup_enabled, owner_id, created_at, updated_at
                FROM workshops
                WHERE id = %s
            """, (workshop_id,))
            
            workshop = cursor.fetchone()
            
            if workshop:
                # Convert datetime to ISO string
                workshop['created_at'] = workshop['created_at'].isoformat() if workshop['created_at'] else None
                workshop['updated_at'] = workshop['updated_at'].isoformat() if workshop['updated_at'] else None
                workshop['workshop_date'] = workshop['workshop_date'].isoformat() if workshop['workshop_date'] else None
                # Convert boolean
                workshop['signup_enabled'] = bool(workshop['signup_enabled'])
            
            return workshop
    
    def get_workshop_by_id(self, workshop_id: str) -> Optional[Dict[str, Any]]:
        """
        Get workshop by ID
        
        Args:
            workshop_id: Workshop ID
            
        Returns:
            Workshop dict or None if not found
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT id, title, description, workshop_date, venue_type, venue_address,
                       status, signup_enabled, owner_id, created_at, updated_at
                FROM workshops
                WHERE id = %s
            """, (workshop_id,))
            
            workshop = cursor.fetchone()
            
            if workshop:
                # Convert datetime to ISO string
                workshop['created_at'] = workshop['created_at'].isoformat() if workshop['created_at'] else None
                workshop['updated_at'] = workshop['updated_at'].isoformat() if workshop['updated_at'] else None
                workshop['workshop_date'] = workshop['workshop_date'].isoformat() if workshop['workshop_date'] else None
                # Convert boolean
                workshop['signup_enabled'] = bool(workshop['signup_enabled'])
            
            return workshop
    
    def get_all_workshops(self) -> List[Dict[str, Any]]:
        """
        Get all workshops
        
        Returns:
            List of workshop dicts
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT id, title, description, workshop_date, venue_type, venue_address,
                       status, signup_enabled, owner_id, created_at, updated_at
                FROM workshops
                ORDER BY created_at DESC
            """)
            
            workshops = cursor.fetchall()
            
            # Convert datetime and boolean fields
            for workshop in workshops:
                workshop['created_at'] = workshop['created_at'].isoformat() if workshop['created_at'] else None
                workshop['updated_at'] = workshop['updated_at'].isoformat() if workshop['updated_at'] else None
                workshop['workshop_date'] = workshop['workshop_date'].isoformat() if workshop['workshop_date'] else None
                workshop['signup_enabled'] = bool(workshop['signup_enabled'])
            
            return workshops
    
    def get_workshops_by_owner(self, owner_id: str) -> List[Dict[str, Any]]:
        """
        Get all workshops owned by a user
        
        Args:
            owner_id: User ID
            
        Returns:
            List of workshop dicts
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT id, title, description, workshop_date, venue_type, venue_address,
                       status, signup_enabled, owner_id, created_at, updated_at
                FROM workshops
                WHERE owner_id = %s
                ORDER BY created_at DESC
            """, (owner_id,))
            
            workshops = cursor.fetchall()
            
            # Convert datetime and boolean fields
            for workshop in workshops:
                workshop['created_at'] = workshop['created_at'].isoformat() if workshop['created_at'] else None
                workshop['updated_at'] = workshop['updated_at'].isoformat() if workshop['updated_at'] else None
                workshop['workshop_date'] = workshop['workshop_date'].isoformat() if workshop['workshop_date'] else None
                workshop['signup_enabled'] = bool(workshop['signup_enabled'])
            
            return workshops
    
    def update_workshop(self, workshop_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Update workshop fields
        
        Args:
            workshop_id: Workshop ID
            updates: Dict of fields to update
            
        Returns:
            Updated workshop dict or None if not found
        """
        # Build dynamic UPDATE query
        allowed_fields = ['title', 'description', 'workshop_date', 'venue_type', 
                         'venue_address', 'status', 'signup_enabled']
        update_fields = []
        values = []
        
        for field in allowed_fields:
            if field in updates:
                update_fields.append(f"{field} = %s")
                values.append(updates[field])
        
        if not update_fields:
            # No valid fields to update, just return current workshop
            return self.get_workshop_by_id(workshop_id)
        
        # Add updated_at
        update_fields.append("updated_at = CURRENT_TIMESTAMP")
        values.append(workshop_id)
        
        with get_db_cursor() as cursor:
            query = f"""
                UPDATE workshops
                SET {', '.join(update_fields)}
                WHERE id = %s
            """
            cursor.execute(query, values)
        
        # Fetch updated workshop (outside the context manager to use a new cursor)
        return self.get_workshop_by_id(workshop_id)
    
    def delete_workshop(self, workshop_id: str) -> bool:
        """
        Delete workshop
        
        Args:
            workshop_id: Workshop ID
            
        Returns:
            True if deleted, False if not found
        """
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM workshops WHERE id = %s", (workshop_id,))
            return cursor.rowcount > 0
