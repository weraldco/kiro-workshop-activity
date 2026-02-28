"""
Password Service - Password hashing and verification using bcrypt
"""
import bcrypt


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt
    
    Args:
        password: Plain text password
        
    Returns:
        Bcrypt hashed password (as string)
    """
    # Generate salt and hash password
    salt = bcrypt.gensalt(rounds=12)  # 12 rounds is secure and performant
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    # Return as string
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """
    Verify a password against a bcrypt hash
    
    Args:
        password: Plain text password to verify
        password_hash: Bcrypt hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    try:
        return bcrypt.checkpw(
            password.encode('utf-8'),
            password_hash.encode('utf-8')
        )
    except Exception:
        # Invalid hash format or other error
        return False
