"""
Challenge service for business logic operations.

This module provides the ChallengeService class that handles challenge-related
business logic including creation and retrieval.
"""

import uuid
from datetime import datetime, timezone

from app.store.workshop_store import WorkshopStore


class ChallengeService:
    """
    Business logic layer for challenge management.
    
    Handles challenge creation with UUID generation and ISO 8601 timestamp
    formatting for workshop-specific challenges.
    """
    
    def __init__(self, store: WorkshopStore):
        """
        Initialize challenge service with data store.
        
        Args:
            store: WorkshopStore instance for data persistence
        """
        self.store = store
    
    def create_challenge(self, workshop_id: str, data: dict) -> dict:
        """
        Create a new challenge for a workshop.
        
        Generates a unique UUID for the challenge and creates an ISO 8601
        timestamp for the creation time.
        
        Args:
            workshop_id: ID of the workshop this challenge belongs to
            data: Challenge data containing title and description
        
        Returns:
            Challenge object with generated ID and timestamp
        """
        # Generate unique ID
        challenge_id = str(uuid.uuid4())
        
        # Create challenge object with all fields
        challenge = {
            'id': challenge_id,
            'workshop_id': workshop_id,
            'title': data['title'],
            'description': data.get('description', ''),
            'created_at': datetime.now(timezone.utc).isoformat()
        }
        
        # Persist to store
        self.store.add_challenge(challenge)
        
        return challenge
    
    def list_challenges(self, workshop_id: str) -> list[dict]:
        """
        Retrieve all challenges for a workshop.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            List of challenge objects for the specified workshop
        """
        return self.store.get_challenges(workshop_id)
