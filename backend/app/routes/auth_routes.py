"""
Authentication Routes
"""
from flask import Blueprint, request, jsonify
from app.store.user_store import UserStore
from app.auth import hash_password, verify_password, generate_access_token
from app.auth.decorators import require_auth
from app.validators import validate_user_registration, validate_user_login

# Create blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Initialize user store
user_store = UserStore()


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user
    
    POST /api/auth/register
    
    Request Body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!",
        "name": "John Doe"
    }
    
    Response (201):
    {
        "id": "uuid",
        "email": "user@example.com",
        "name": "John Doe",
        "access_token": "jwt-token",
        "token_type": "Bearer"
    }
    
    Errors:
    - 400: Invalid input (validation error)
    - 409: Email already exists
    - 500: Server error
    """
    try:
        # Get request data
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({
                "error": "Request body is required",
                "code": "MISSING_BODY",
                "status": 400
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validate input
        is_valid, error_message = validate_user_registration(email, password, name)
        if not is_valid:
            return jsonify({
                "error": error_message,
                "code": "VALIDATION_ERROR",
                "status": 400
            }), 400
        
        # Hash password
        password_hash = hash_password(password)
        
        # Create user
        try:
            user = user_store.create_user(email, password_hash, name)
        except ValueError as e:
            # Duplicate email
            return jsonify({
                "error": str(e),
                "code": "EMAIL_EXISTS",
                "status": 409
            }), 409
        
        # Generate access token
        access_token = generate_access_token(
            user_id=user['id'],
            email=user['email'],
            name=user['name']
        )
        
        # Return user with token
        return jsonify({
            "id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "created_at": user['created_at'],
            "access_token": access_token,
            "token_type": "Bearer"
        }), 201
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user
    
    POST /api/auth/login
    
    Request Body:
    {
        "email": "user@example.com",
        "password": "SecurePass123!"
    }
    
    Response (200):
    {
        "id": "uuid",
        "email": "user@example.com",
        "name": "John Doe",
        "access_token": "jwt-token",
        "token_type": "Bearer"
    }
    
    Errors:
    - 400: Missing email or password
    - 401: Invalid credentials
    - 500: Server error
    """
    try:
        # Get request data
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({
                "error": "Request body is required",
                "code": "MISSING_BODY",
                "status": 400
            }), 400
        
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        # Validate input
        is_valid, error_message = validate_user_login(email, password)
        if not is_valid:
            return jsonify({
                "error": error_message,
                "code": "VALIDATION_ERROR",
                "status": 400
            }), 400
        
        # Get user by email
        user = user_store.get_user_by_email(email)
        
        if not user:
            return jsonify({
                "error": "Invalid email or password",
                "code": "INVALID_CREDENTIALS",
                "status": 401
            }), 401
        
        # Verify password
        if not verify_password(password, user['password_hash']):
            return jsonify({
                "error": "Invalid email or password",
                "code": "INVALID_CREDENTIALS",
                "status": 401
            }), 401
        
        # Generate access token
        access_token = generate_access_token(
            user_id=user['id'],
            email=user['email'],
            name=user['name']
        )
        
        # Return user with token (without password_hash)
        return jsonify({
            "id": user['id'],
            "email": user['email'],
            "name": user['name'],
            "created_at": user['created_at'],
            "access_token": access_token,
            "token_type": "Bearer"
        }), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@auth_bp.route('/me', methods=['GET'])
@require_auth
def get_current_user():
    """
    Get current user information
    
    GET /api/auth/me
    
    Headers:
        Authorization: Bearer <access-token>
    
    Response (200):
    {
        "id": "uuid",
        "email": "user@example.com",
        "name": "John Doe",
        "created_at": "ISO-8601"
    }
    
    Errors:
    - 401: Missing or invalid token
    - 404: User not found
    - 500: Server error
    """
    try:
        # Get current user from request context (set by @require_auth decorator)
        current_user = request.current_user
        
        # Get full user details from database
        user = user_store.get_user_by_id(current_user['id'])
        
        if not user:
            return jsonify({
                "error": "User not found",
                "code": "USER_NOT_FOUND",
                "status": 404
            }), 404
        
        return jsonify(user), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500
