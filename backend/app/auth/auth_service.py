"""
Auth Service - JWT token generation and verification
"""
import os
import jwt
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# JWT Configuration
JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-secret-key-change-in-production')
JWT_ALGORITHM = os.getenv('JWT_ALGORITHM', 'HS256')
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', '30'))


def generate_access_token(user_id: str, email: str, name: str) -> str:
    """
    Generate a JWT access token
    
    Args:
        user_id: User ID
        email: User email
        name: User name
        
    Returns:
        JWT token string
    """
    # Calculate expiration time
    expire = datetime.now(timezone.utc) + timedelta(minutes=JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Create payload
    payload = {
        'user_id': user_id,
        'email': email,
        'name': name,
        'exp': expire,
        'iat': datetime.now(timezone.utc)
    }
    
    # Generate token
    token = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    
    return token


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode a JWT token
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload dict if valid, None if invalid/expired
    """
    try:
        # Decode and verify token
        payload = jwt.decode(
            token,
            JWT_SECRET_KEY,
            algorithms=[JWT_ALGORITHM]
        )
        
        return payload
    
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    
    except jwt.InvalidTokenError:
        # Token is invalid
        return None
    
    except Exception:
        # Other errors
        return None


def decode_token_without_verification(token: str) -> Optional[Dict[str, Any]]:
    """
    Decode a JWT token without verification (for debugging/testing only)
    
    Args:
        token: JWT token string
        
    Returns:
        Decoded payload dict, or None if invalid format
    """
    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return payload
    except Exception:
        return None
