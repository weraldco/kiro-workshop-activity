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
    - description: string (required)
    - html_content: string (required, including empty string)
    
    Args:
        data: Dictionary containing challenge data
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    # Check for required fields
    required_fields = ['title', 'description', 'html_content']
    missing_fields = [field for field in required_fields if field not in data]
    
    if missing_fields:
        return False, f"Missing required fields: {', '.join(missing_fields)}"
    
    # Validate title
    title = data.get('title')
    if not isinstance(title, str):
        return False, "Title must be a string"
    if not title or not title.strip():
        return False, "Title must be a non-empty string"
    
    # Validate description
    description = data.get('description')
    if not isinstance(description, str):
        return False, "Description must be a string"
    
    # Validate html_content
    html_content = data.get('html_content')
    is_valid, error_message = validate_html_content(html_content)
    if not is_valid:
        return False, error_message
    
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


def validate_status(status: Any) -> tuple[bool, str]:
    """
    Validates workshop status is one of: pending, ongoing, completed.
    
    Args:
        status: The status value to validate
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    if not isinstance(status, str):
        return False, "Status must be one of: pending, ongoing, completed"
    
    if status not in ["pending", "ongoing", "completed"]:
        return False, "Status must be one of: pending, ongoing, completed"
    
    return True, ""


def validate_signup_enabled(signup_enabled: Any) -> tuple[bool, str]:
    """
    Validates signup_enabled is a boolean value.
    
    Args:
        signup_enabled: The signup_enabled value to validate
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    if not isinstance(signup_enabled, bool):
        return False, "signup_enabled must be a boolean value"
    
    return True, ""


def validate_html_content(html_content: Any) -> tuple[bool, str]:
    """
    Validates html_content is a string (including empty string).
    Includes maximum length validation (50KB) to prevent DoS attacks.
    
    Args:
        html_content: The html_content value to validate
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    if not isinstance(html_content, str):
        return False, "html_content must be a string"
    
    # Maximum length: 50KB (50 * 1024 bytes)
    max_length = 50 * 1024
    if len(html_content.encode('utf-8')) > max_length:
        return False, f"html_content must not exceed {max_length} bytes (50KB)"
    
    return True, ""


def validate_email_format(email: Any) -> tuple[bool, str]:
    """
    Validates email format using basic regex pattern.
    
    Args:
        email: The email address to validate
        
    Returns:
        (is_valid, error_message): Tuple with validation result and error message
    """
    import re
    
    if not isinstance(email, str):
        return False, "Email must be a string"
    
    # Basic email regex pattern
    # Matches: local-part@domain.tld
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(email_pattern, email):
        return False, "Invalid email format"
    
    return True, ""


# ============================================================================
# User Validation
# ============================================================================

def validate_email(email: str) -> tuple[bool, str]:
    """
    Validate email format
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import re
    
    if not email:
        return False, "Email is required"
    
    if not isinstance(email, str):
        return False, "Email must be a string"
    
    # Basic email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if not re.match(pattern, email):
        return False, "Invalid email format"
    
    if len(email) > 255:
        return False, "Email must be less than 255 characters"
    
    return True, ""


def validate_password(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    
    Requirements:
    - Minimum 8 characters
    - At least 1 uppercase letter
    - At least 1 lowercase letter
    - At least 1 number
    - At least 1 special character (!@#$%^&*()_+-=[]{}|;:,.<>?)
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    import re
    
    if not password:
        return False, "Password is required"
    
    if not isinstance(password, str):
        return False, "Password must be a string"
    
    if len(password) < 8:
        return False, "Password must be at least 8 characters"
    
    if len(password) > 128:
        return False, "Password must be less than 128 characters"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one number"
    
    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>?]', password):
        return False, "Password must contain at least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)"
    
    return True, ""


def validate_user_name(name: str) -> tuple[bool, str]:
    """
    Validate user name
    
    Args:
        name: User name to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not name:
        return False, "Name is required"
    
    if not isinstance(name, str):
        return False, "Name must be a string"
    
    name = name.strip()
    
    if len(name) < 1:
        return False, "Name cannot be empty"
    
    if len(name) > 100:
        return False, "Name must be less than 100 characters"
    
    return True, ""


def validate_user_registration(email: str, password: str, name: str) -> tuple[bool, str]:
    """
    Validate user registration data
    
    Args:
        email: Email address
        password: Password
        name: User name
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Validate email
    is_valid, error = validate_email(email)
    if not is_valid:
        return False, error
    
    # Validate password
    is_valid, error = validate_password(password)
    if not is_valid:
        return False, error
    
    # Validate name
    is_valid, error = validate_user_name(name)
    if not is_valid:
        return False, error
    
    return True, ""


def validate_user_login(email: str, password: str) -> tuple[bool, str]:
    """
    Validate user login data
    
    Args:
        email: Email address
        password: Password
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not email:
        return False, "Email is required"
    
    if not password:
        return False, "Password is required"
    
    return True, ""
