"""
Registration service for business logic operations.

This module provides the RegistrationService class that handles registration-related
business logic including participant registration with capacity checking.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, Tuple

from app.store.workshop_store import WorkshopStore
from app.validators import validate_email_format


class RegistrationService:
    """
    Business logic layer for registration management.
    
    Handles participant registration with capacity checking, registration count
    increment, and ISO 8601 timestamp formatting.
    """
    
    def __init__(self, store: WorkshopStore):
        """
        Initialize registration service with data store.
        
        Args:
            store: WorkshopStore instance for data persistence
        """
        self.store = store
    
    def register_participant(self, workshop_id: str, data: dict) -> Tuple[Optional[dict], str]:
        """
        Register a participant for a workshop.
        
        Checks workshop capacity before registration. If the workshop is at
        capacity, returns None with an error message. Otherwise, creates the
        registration, increments the workshop's registration count, and returns
        the registration object.
        
        Args:
            workshop_id: ID of the workshop to register for
            data: Registration data containing participant_name and participant_email
        
        Returns:
            Tuple of (Registration object with ID, error_message)
            If successful: (registration_dict, "")
            If failed: (None, error_message)
        """
        # Get the workshop (first check - 404 if not exists)
        workshop = self.store.get_workshop(workshop_id)
        
        if workshop is None:
            return None, f"Workshop with ID '{workshop_id}' does not exist"
        
        # Validate email format (after workshop exists check)
        participant_email = data.get('participant_email', '')
        is_valid, error_msg = validate_email_format(participant_email)
        if not is_valid:
            return None, error_msg
        
        # Check signup_enabled (second validation after workshop exists)
        signup_enabled = workshop.get('signup_enabled', True)
        if not signup_enabled:
            return None, "Signups are currently disabled for this workshop"
        
        # Check status (third validation - after signup_enabled, before capacity)
        status = workshop.get('status', 'pending')
        if status == 'ongoing':
            return None, "Signups are closed for ongoing workshops"
        elif status == 'completed':
            return None, "Signups are closed for completed workshops"
        # Only allow registration when status is "pending"
        
        # Check capacity (fourth validation)
        current_count = workshop.get('registration_count', 0)
        capacity = workshop['capacity']
        
        if current_count >= capacity:
            return None, "Workshop is full. Registration count has reached capacity."
        
        # Generate unique ID
        registration_id = str(uuid.uuid4())
        
        # Create registration object with all fields
        registration = {
            'id': registration_id,
            'workshop_id': workshop_id,
            'participant_name': data['participant_name'],
            'participant_email': data['participant_email'],
            'registered_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Persist registration to store
        self.store.add_registration(registration)
        
        # Increment workshop registration count
        workshop['registration_count'] = current_count + 1
        self.store.update_workshop(workshop)
        
        return registration, ""
    
    def list_registrations(self) -> list[dict]:
        """
        Retrieve all registrations.
        
        Returns:
            List of registration objects
        """
        return self.store.get_all_registrations()
    
    def get_registration_count(self, workshop_id: str) -> int:
        """
        Get current registration count for a workshop.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            Number of registrations for the workshop
        """
        registrations = self.store.get_registrations_for_workshop(workshop_id)
        return len(registrations)
    
    def get_registrations_for_workshop(self, workshop_id: str) -> list[dict]:
        """
        Get all registrations for a workshop.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            List of registration objects for the workshop
        """
        return self.store.get_registrations_for_workshop(workshop_id)
