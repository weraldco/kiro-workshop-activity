"""
Workshop data store with JSON file persistence.

This module provides the WorkshopStore class that manages all data persistence
to a JSON file in the project directory. It uses file locking to ensure
thread-safe operations and prevent data corruption during concurrent access.
"""

import json
import os
from typing import Optional

from app.store.file_lock import FileLock


class WorkshopStore:
    """
    Data access layer for workshop management system.
    
    Provides thread-safe JSON file operations for workshops, challenges,
    and registrations. All write operations use file locking to ensure
    atomicity and prevent data corruption.
    """
    
    def __init__(self, file_path: str):
        """
        Initialize store with JSON file path.
        
        Creates the JSON file with empty structure if it doesn't exist.
        
        Args:
            file_path: Path to the JSON file for data persistence
        """
        self.file_path = file_path
        
        # Initialize file with empty structure if it doesn't exist
        if not os.path.exists(file_path):
            self._initialize_file()
    
    def _initialize_file(self) -> None:
        """
        Create JSON file with empty data structure.
        
        Initializes the file with empty arrays for workshops, challenges,
        and registrations.
        """
        initial_data = {
            "workshops": [],
            "challenges": [],
            "registrations": []
        }
        
        with FileLock(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump(initial_data, f, indent=2)
    
    def load_data(self) -> dict:
        """
        Load all data from JSON file.
        
        Returns:
            Dictionary with workshops, challenges, and registrations arrays
        """
        if not os.path.exists(self.file_path):
            self._initialize_file()
        
        # Check if file is empty or invalid
        try:
            with open(self.file_path, 'r') as f:
                content = f.read().strip()
                if not content:
                    self._initialize_file()
                    with open(self.file_path, 'r') as f2:
                        return json.load(f2)
                return json.loads(content)
        except json.JSONDecodeError:
            # File exists but contains invalid JSON, reinitialize
            self._initialize_file()
            with open(self.file_path, 'r') as f:
                return json.load(f)
    
    def save_data(self, data: dict) -> None:
        """
        Save all data to JSON file with file locking.
        
        Uses file locking to ensure atomic write operations and prevent
        data corruption during concurrent access.
        
        Args:
            data: Dictionary containing workshops, challenges, and registrations
        """
        with FileLock(self.file_path):
            with open(self.file_path, 'w') as f:
                json.dump(data, f, indent=2)
    
    def add_workshop(self, workshop: dict) -> None:
        """
        Add a workshop to the store.
        
        Args:
            workshop: Workshop dictionary with all required fields
        """
        data = self.load_data()
        data['workshops'].append(workshop)
        self.save_data(data)
    
    def get_workshop(self, workshop_id: str) -> Optional[dict]:
        """
        Retrieve a workshop by ID.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            Workshop dictionary if found, None otherwise
        """
        data = self.load_data()
        for workshop in data['workshops']:
            if workshop['id'] == workshop_id:
                return workshop
        return None
    
    def get_all_workshops(self) -> list[dict]:
        """
        Retrieve all workshops.
        
        Returns:
            List of workshop dictionaries
        """
        data = self.load_data()
        return data['workshops']
    
    def add_challenge(self, challenge: dict) -> None:
        """
        Add a challenge to the store.
        
        Args:
            challenge: Challenge dictionary with all required fields
        """
        data = self.load_data()
        data['challenges'].append(challenge)
        self.save_data(data)
    
    def get_challenges(self, workshop_id: str) -> list[dict]:
        """
        Retrieve all challenges for a workshop.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            List of challenge dictionaries for the specified workshop
        """
        data = self.load_data()
        return [c for c in data['challenges'] if c['workshop_id'] == workshop_id]
    
    def add_registration(self, registration: dict) -> None:
        """
        Add a registration to the store.
        
        Args:
            registration: Registration dictionary with all required fields
        """
        data = self.load_data()
        data['registrations'].append(registration)
        self.save_data(data)
    
    def get_all_registrations(self) -> list[dict]:
        """
        Retrieve all registrations.
        
        Returns:
            List of registration dictionaries
        """
        data = self.load_data()
        return data['registrations']
    
    def get_registrations_for_workshop(self, workshop_id: str) -> list[dict]:
        """
        Retrieve all registrations for a specific workshop.
        
        Args:
            workshop_id: Unique identifier of the workshop
        
        Returns:
            List of registration dictionaries for the specified workshop
        """
        data = self.load_data()
        return [r for r in data['registrations'] if r['workshop_id'] == workshop_id]
    
    def update_workshop(self, workshop: dict) -> None:
        """
        Update an existing workshop in the store.
        
        Finds the workshop by ID and replaces it with the updated version.
        
        Args:
            workshop: Workshop dictionary with updated fields
        """
        data = self.load_data()
        
        # Find and update the workshop
        for i, w in enumerate(data['workshops']):
            if w['id'] == workshop['id']:
                data['workshops'][i] = workshop
                break
        
        self.save_data(data)
