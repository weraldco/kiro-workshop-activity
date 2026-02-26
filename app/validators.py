"""
Input validation functions for workshop management API.

This module provides validation functions that return (is_valid, error_message) tuples.
"""

from datetime import datetime
from typing import Any


def validate_delivery_mode(mode: Any) -> bool:
    """
    Validates delivery mode is one of: online, face-to-face, hybrid.
    
    Args:
        mode: The delivery mode to validate
        
    Returns:
        True if valid, False otherwise
    """
    if not isinstance(mode, str):
        return False
    return mode in ["online", "face-to-face", "hybrid"]


def validate_time_range(start_time: Any, end_time: Any) -> bool:
    """
    Validates that start_time occurs before end_time.
    
    Args:
        start_time: The start time (ISO 8601 string or datetime)
        end_time: The end time (ISO 8601 string or datetime)
        
    Returns:
        True if valid (start < end), False otherwise
    """
    try:
        # Handle both string and datetime inputs
        if isinstance(start_time, str):
            start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        elif isinstance(start_time, datetime):
            start_dt = start_time
        else:
            return False
            
        if isinstance(end_time, str):
            end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        elif isinstance(end_time, datetime):
            end_dt = end_time
        else:
            return False
            
        return start_dt < end_dt
    except (ValueError, AttributeError):
        return False


def validate_workshop_data(data: dict) -> tuple[bool, str]:
    """
    Validates workshop creation data.
    
    Validates:
    - title: non-empty string
    - start_time: occurs before end_time
    - capacity: positive integer
    - delivery_mode: one of "online", "face-to-face", "hybrid"
    - required fields are present
    
    Args:
        data: Dictionary containing workshop data
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    # Check for required fields
    required_fields = ['title', 'start_time', 'end_time', 'capacity', 'delivery_mode']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate title
    title = data.get('title')
    if not isinstance(title, str):
        return False, "Title must be a string"
    if not title or not title.strip():
        return False, "Title must be a non-empty string"
    
    # Validate capacity
    capacity = data.get('capacity')
    if not isinstance(capacity, int):
        return False, "Capacity must be an integer"
    if capacity <= 0:
        return False, "Capacity must be a positive integer"
    
    # Validate delivery mode
    delivery_mode = data.get('delivery_mode')
    if not validate_delivery_mode(delivery_mode):
        return False, "Delivery mode must be one of: online, face-to-face, hybrid"
    
    # Validate time range
    start_time = data.get('start_time')
    end_time = data.get('end_time')
    if not validate_time_range(start_time, end_time):
        return False, "Start time must occur before end time"
    
    return True, ""


def validate_challenge_data(data: dict) -> tuple[bool, str]:
    """
    Validates challenge creation data.
    
    Validates:
    - title: non-empty string
    
    Args:
        data: Dictionary containing challenge data
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    # Check for required fields
    if 'title' not in data:
        return False, "Missing required field: title"
    
    # Validate title
    title = data.get('title')
    if not isinstance(title, str):
        return False, "Title must be a string"
    if not title or not title.strip():
        return False, "Title must be a non-empty string"
    
    return True, ""


def validate_registration_data(data: dict) -> tuple[bool, str]:
    """
    Validates registration data.
    
    Validates:
    - required fields are present (participant_name, participant_email)
    
    Args:
        data: Dictionary containing registration data
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    # Check for required fields
    required_fields = ['participant_name', 'participant_email']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    return True, ""
