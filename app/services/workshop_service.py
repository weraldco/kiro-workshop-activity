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
    
    def create_workshop(self, data: dict) -> dict:
        """
        Create a new workshop with generated ID and initial registration count.
        
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
