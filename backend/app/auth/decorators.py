"""
Auth Decorators - Route protection decorators
"""
from functools import wraps
from flask import request, jsonify
from app.auth.auth_service import verify_token


def require_auth(f):
    """
    Decorator to require authentication for a route
    
    Usage:
        @app.route('/protected')
        @require_auth
        def protected_route():
            user = request.current_user
            return jsonify({"message": f"Hello {user['name']}"})
    
    The decorator:
    - Extracts JWT token from Authorization header
    - Verifies the token
    - Adds user data to request.current_user
    - Returns 401 if token is missing or invalid
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return jsonify({
                "error": "Missing authorization token",
                "code": "UNAUTHORIZED",
                "status": 401
            }), 401
        
        # Check format: "Bearer <token>"
        parts = auth_header.split()
        
        if len(parts) != 2 or parts[0].lower() != 'bearer':
            return jsonify({
                "error": "Invalid authorization header format. Expected: Bearer <token>",
                "code": "INVALID_AUTH_HEADER",
                "status": 401
            }), 401
        
        token = parts[1]
        
        # Verify token
        payload = verify_token(token)
        
        if not payload:
            return jsonify({
                "error": "Invalid or expired token",
                "code": "INVALID_TOKEN",
                "status": 401
            }), 401
        
        # Add user data to request context
        request.current_user = {
            'id': payload.get('user_id'),
            'email': payload.get('email'),
            'name': payload.get('name')
        }
        
        # Call the actual route function
        return f(*args, **kwargs)
    
    return decorated_function


def optional_auth(f):
    """
    Decorator to optionally extract user from token if present
    
    Usage:
        @app.route('/public-but-personalized')
        @optional_auth
        def route():
            user = getattr(request, 'current_user', None)
            if user:
                return jsonify({"message": f"Hello {user['name']}"})
            else:
                return jsonify({"message": "Hello guest"})
    
    The decorator:
    - Extracts JWT token from Authorization header if present
    - Verifies the token if present
    - Adds user data to request.current_user if valid
    - Does NOT return error if token is missing or invalid
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Extract token from Authorization header
        auth_header = request.headers.get('Authorization')
        
        if auth_header:
            parts = auth_header.split()
            
            if len(parts) == 2 and parts[0].lower() == 'bearer':
                token = parts[1]
                payload = verify_token(token)
                
                if payload:
                    request.current_user = {
                        'id': payload.get('user_id'),
                        'email': payload.get('email'),
                        'name': payload.get('name')
                    }
        
        # Call the actual route function (even if no valid token)
        return f(*args, **kwargs)
    
    return decorated_function
