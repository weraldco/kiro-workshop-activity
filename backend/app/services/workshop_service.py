"""
Workshop service for business logic operations.

This module provides the WorkshopService class that handles workshop-related
business logic including creation, retrieval, and validation.
"""

import uuid
from datetime import datetime
from typing import Optional

from app.store.workshop_store import WorkshopStore


class WorkshopService:
    """
    Business logic layer for workshop management.
    
    Handles workshop creation with UUID generation, registration count
    initialization, and ISO 8601 timestamp formatting.
    """
    
    def __init__(self, store: WorkshopStore):
        """
        Initialize workshop service with data store.
        
        Args:
            store: WorkshopStore instance for data persistence
        """
        self.store = store
    
    def create_workshop_v2(self, data: dict) -> dict:
        """
        Create a new workshop with TypeScript API schema.
        
        Generates a unique UUID for the workshop and initializes with
        status='pending' and signup_enabled=true.
        
        Args:
            data: Workshop data containing title and description
        
        Returns:
            Workshop object with TypeScript API schema
        """
        # Generate unique ID
        workshop_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat() + 'Z'
        
        # Create workshop object with TypeScript API schema
        workshop = {
            'id': workshop_id,
            'title': data['title'].strip(),
            'description': data['description'].strip(),
            'status': 'pending',
            'signup_enabled': True,
            'created_at': now,
            'updated_at': now
        }
        
        # Persist to store
        self.store.add_workshop(workshop)
        
        return workshop
    
    def list_workshops_v2(self) -> list[dict]:
        """
        Retrieve all workshops with TypeScript API schema.
        
        Returns:
            List of workshop objects
        """
        workshops = self.store.get_all_workshops()
        
        # Ensure all workshops have the required fields
        result = []
        for workshop in workshops:
            # If workshop has old schema, skip or convert
            if 'status' in workshop and 'signup_enabled' in workshop:
                result.append(workshop)
            # Optionally convert old schema to new schema
            elif 'start_time' in workshop:
                # Convert old workshop to new schema
                result.append({
                    'id': workshop['id'],
                    'title': workshop['title'],
                    'description': workshop.get('description', ''),
                    'status': workshop.get('status', 'pending'),
                    'signup_enabled': workshop.get('signup_enabled', True),
                    'created_at': workshop.get('created_at', datetime.utcnow().isoformat() + 'Z'),
                    'updated_at': workshop.get('updated_at', datetime.utcnow().isoformat() + 'Z')
                })
        
        return result
    
    def create_workshop(self, data: dict) -> dict:
        """
        Create a new workshop with legacy schema (for backward compatibility).
        
        Generates a unique UUID for the workshop and initializes the
        registration count to zero. Ensures timestamps are in ISO 8601 format.
        
        Args:
            data: Workshop data containing title, description, start_time,
                  end_time, capacity, and delivery_mode
        
        Returns:
            Workshop object with generated ID and registration_count
        """
        # Generate unique ID
        workshop_id = str(uuid.uuid4())
        
        # Create workshop object with all fields
        workshop = {
            'id': workshop_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'start_time': self._ensure_iso8601(data['start_time']),
            'end_time': self._ensure_iso8601(data['end_time']),
            'capacity': data['capacity'],
            'delivery_mode': data['delivery_mode'],
            'registration_count': 0  # Initialize to zero
        }
        
        # Persist to store
        self.store.add_workshop(workshop)
        
        return workshop
    
    def get_workshop(self, workshop_id: str) -> Optional[dict]:
        """
        Retrieve a workshop by ID.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            Workshop object if found, None otherwise
        """
        return self.store.get_workshop(workshop_id)
    
    def list_workshops(self) -> list[dict]:
        """
        Retrieve all workshops.
        
        Returns:
            List of workshop objects
        """
        return self.store.get_all_workshops()
    
    def workshop_exists(self, workshop_id: str) -> bool:
        """
        Check if a workshop exists.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            True if workshop exists, False otherwise
        """
        return self.store.get_workshop(workshop_id) is not None
    
    def update_workshop(self, workshop: dict) -> None:
        """
        Update an existing workshop.
        
        Args:
            workshop: Workshop dictionary with updated fields
        """
        self.store.update_workshop(workshop)
    
    def _ensure_iso8601(self, timestamp: str) -> str:
        """
        Ensure timestamp is in ISO 8601 format.
        
        If the timestamp is already a string, returns it as-is.
        If it's a datetime object, converts it to ISO 8601 format.
        
        Args:
            timestamp: Timestamp string or datetime object
        
        Returns:
            ISO 8601 formatted timestamp string
        """
        if isinstance(timestamp, datetime):
            return timestamp.isoformat()
        return timestamp
