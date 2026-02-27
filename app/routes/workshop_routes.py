"""
Workshop routes for the Flask API.

This module provides all workshop-related endpoints including workshop creation,
retrieval, challenge creation, and participant registration.
"""

from flask import Blueprint, request, jsonify, current_app, abort
from werkzeug.exceptions import BadRequest

from app.validators import validate_workshop_data, validate_challenge_data, validate_registration_data
from app.services.workshop_service import WorkshopService
from app.services.challenge_service import ChallengeService
from app.services.registration_service import RegistrationService
from app.store.workshop_store import WorkshopStore


# Create blueprint
workshop_bp = Blueprint('workshop', __name__)


def get_services():
    """
    Helper function to initialize services with the configured store.
    
    Returns:
        Tuple of (WorkshopService, ChallengeService, RegistrationService)
    """
    store = WorkshopStore(current_app.config['JSON_FILE_PATH'])
    workshop_service = WorkshopService(store)
    challenge_service = ChallengeService(store)
    registration_service = RegistrationService(store)
    return workshop_service, challenge_service, registration_service


@workshop_bp.route('/api/workshop', methods=['POST'])
def create_workshop():
    """
    Create a new workshop.
    
    Request body:
        {
            "title": "string",
            "description": "string",
            "start_time": "ISO 8601 string",
            "end_time": "ISO 8601 string",
            "capacity": integer,
            "delivery_mode": "online|face-to-face|hybrid"
        }
    
    Returns:
        201: {"success": true, "data": {workshop object}}
        400: {"success": false, "error": "error message", "data": {}}
    """
    try:
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON",
                "data": {}
            }), 400
        
        # Validate workshop data
        is_valid, error_message = validate_workshop_data(data)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message,
                "data": {}
            }), 400
        
        # Create workshop
        workshop_service, _, _ = get_services()
        workshop = workshop_service.create_workshop(data)
        
        return jsonify({
            "success": True,
            "data": workshop
        }), 201
        
    except BadRequest:
        # Handle malformed JSON
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON",
            "data": {}
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500


@workshop_bp.route('/api/workshop', methods=['GET'])
def list_workshops():
    """
    List all workshops.
    
    Returns:
        200: {"success": true, "data": [workshop objects]}
    """
    try:
        workshop_service, _, _ = get_services()
        workshops = workshop_service.list_workshops()
        
        return jsonify({
            "success": True,
            "data": workshops
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500


@workshop_bp.route('/api/workshop/<workshop_id>', methods=['GET'])
def get_workshop(workshop_id):
    """
    Get a specific workshop by ID.
    
    Args:
        workshop_id: Unique identifier of the workshop
    
    Returns:
        200: {"success": true, "data": {workshop object}}
        404: {"success": false, "error": "error message", "data": {}}
    """
    try:
        workshop_service, _, _ = get_services()
        workshop = workshop_service.get_workshop(workshop_id)
        
        if workshop is None:
            return jsonify({
                "success": False,
                "error": f"Workshop with ID '{workshop_id}' does not exist",
                "data": {}
            }), 404
        
        return jsonify({
            "success": True,
            "data": workshop
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500



@workshop_bp.route('/api/workshop/<workshop_id>/challenge', methods=['POST'])
def create_challenge(workshop_id):
    """
    Create a new challenge for a workshop.
    
    Args:
        workshop_id: Unique identifier of the workshop
    
    Request body:
        {
            "title": "string",
            "description": "string"
        }
    
    Returns:
        201: {"success": true, "data": {challenge object}}
        400: {"success": false, "error": "error message", "data": {}}
        404: {"success": false, "error": "error message", "data": {}}
    """
    try:
        # Check if workshop exists
        workshop_service, challenge_service, _ = get_services()
        if not workshop_service.workshop_exists(workshop_id):
            return jsonify({
                "success": False,
                "error": f"Workshop with ID '{workshop_id}' does not exist",
                "data": {}
            }), 404
        
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON",
                "data": {}
            }), 400
        
        # Validate challenge data
        is_valid, error_message = validate_challenge_data(data)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message,
                "data": {}
            }), 400
        
        # Create challenge
        challenge = challenge_service.create_challenge(workshop_id, data)
        
        return jsonify({
            "success": True,
            "data": challenge
        }), 201
        
    except BadRequest:
        # Handle malformed JSON
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON",
            "data": {}
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500



@workshop_bp.route('/api/workshop/<workshop_id>/register', methods=['POST'])
def register_for_workshop(workshop_id):
    """
    Register a participant for a workshop.
    
    Args:
        workshop_id: Unique identifier of the workshop
    
    Request body:
        {
            "participant_name": "string",
            "participant_email": "string"
        }
    
    Returns:
        201: {"success": true, "data": {registration object}}
        400: {"success": false, "error": "error message", "data": {}}
        404: {"success": false, "error": "error message", "data": {}}
        409: {"success": false, "error": "error message", "data": {}}
    """
    try:
        # Check if workshop exists
        workshop_service, _, registration_service = get_services()
        if not workshop_service.workshop_exists(workshop_id):
            return jsonify({
                "success": False,
                "error": f"Workshop with ID '{workshop_id}' does not exist",
                "data": {}
            }), 404
        
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON",
                "data": {}
            }), 400
        
        # Validate registration data
        is_valid, error_message = validate_registration_data(data)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message,
                "data": {}
            }), 400
        
        # Register participant
        registration, error = registration_service.register_participant(workshop_id, data)
        
        if registration is None:
            # Check error type and return appropriate status code
            if "full" in error.lower() or "capacity" in error.lower():
                # Capacity error - 409
                return jsonify({
                    "success": False,
                    "error": error,
                    "data": {}
                }), 409
            elif "disabled" in error.lower() or "closed" in error.lower():
                # Signup disabled or status-based closure - 403
                return jsonify({
                    "success": False,
                    "error": error,
                    "data": {}
                }), 403
            else:
                # Other errors (validation, etc.) - 400
                return jsonify({
                    "success": False,
                    "error": error,
                    "data": {}
                }), 400
        
        return jsonify({
            "success": True,
            "data": registration
        }), 201
        
    except BadRequest:
        # Handle malformed JSON
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON",
            "data": {}
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500


@workshop_bp.route('/api/workshop/registrations', methods=['GET'])
def list_registrations():
    """
    List all registrations.
    
    Returns:
        200: {"success": true, "data": [registration objects]}
    """
    try:
        _, _, registration_service = get_services()
        registrations = registration_service.list_registrations()
        
        return jsonify({
            "success": True,
            "data": registrations
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500


@workshop_bp.route('/api/workshop/<workshop_id>/status', methods=['PATCH'])
def update_workshop_status(workshop_id):
    """
    Update workshop status.
    
    SECURITY NOTE: No authorization check - any user can update status.
    
    Args:
        workshop_id: Unique identifier of the workshop
    
    Request body:
        {
            "status": "pending|ongoing|completed"
        }
    
    Returns:
        200: {"success": true, "data": {workshop object}}
        400: {"success": false, "error": "error message", "data": {}}
        404: {"success": false, "error": "error message", "data": {}}
    """
    try:
        from app.validators import validate_status
        
        # Check if workshop exists
        workshop_service, _, _ = get_services()
        workshop = workshop_service.get_workshop(workshop_id)
        
        if workshop is None:
            return jsonify({
                "success": False,
                "error": f"Workshop with ID '{workshop_id}' does not exist",
                "data": {}
            }), 404
        
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON",
                "data": {}
            }), 400
        
        if 'status' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: status",
                "data": {}
            }), 400
        
        # Validate status value
        is_valid, error_message = validate_status(data['status'])
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message,
                "data": {}
            }), 400
        
        # Update workshop status
        workshop['status'] = data['status']
        workshop_service.update_workshop(workshop)
        
        return jsonify({
            "success": True,
            "data": workshop
        }), 200
        
    except BadRequest:
        # Handle malformed JSON
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON",
            "data": {}
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500


@workshop_bp.route('/api/workshop/<workshop_id>/signup', methods=['PATCH'])
def update_workshop_signup(workshop_id):
    """
    Update workshop signup_enabled flag.
    
    SECURITY NOTE: No authorization check - any user can toggle signups.
    
    Args:
        workshop_id: Unique identifier of the workshop
    
    Request body:
        {
            "signup_enabled": true|false
        }
    
    Returns:
        200: {"success": true, "data": {workshop object}}
        400: {"success": false, "error": "error message", "data": {}}
        404: {"success": false, "error": "error message", "data": {}}
    """
    try:
        from app.validators import validate_signup_enabled
        
        # Check if workshop exists
        workshop_service, _, _ = get_services()
        workshop = workshop_service.get_workshop(workshop_id)
        
        if workshop is None:
            return jsonify({
                "success": False,
                "error": f"Workshop with ID '{workshop_id}' does not exist",
                "data": {}
            }), 404
        
        data = request.get_json()
        
        if data is None:
            return jsonify({
                "success": False,
                "error": "Request body must be valid JSON",
                "data": {}
            }), 400
        
        if 'signup_enabled' not in data:
            return jsonify({
                "success": False,
                "error": "Missing required field: signup_enabled",
                "data": {}
            }), 400
        
        # Validate signup_enabled value
        is_valid, error_message = validate_signup_enabled(data['signup_enabled'])
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message,
                "data": {}
            }), 400
        
        # Update workshop signup_enabled
        workshop['signup_enabled'] = data['signup_enabled']
        workshop_service.update_workshop(workshop)
        
        return jsonify({
            "success": True,
            "data": workshop
        }), 200
        
    except BadRequest:
        # Handle malformed JSON
        return jsonify({
            "success": False,
            "error": "Request body must be valid JSON",
            "data": {}
        }), 400
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500


@workshop_bp.route('/api/workshop/<workshop_id>/challenges', methods=['GET'])
def get_workshop_challenges(workshop_id):
    """
    Retrieve challenges for a workshop (enrolled participants only, ongoing workshops only).
    
    SECURITY NOTE: Email is NOT verified - any user can claim any email.
    
    Args:
        workshop_id: Unique identifier of the workshop
    
    Query parameters:
        email: Participant email address for enrollment verification
    
    Returns:
        200: {"success": true, "data": [challenge objects]}
        400: {"success": false, "error": "error message", "data": {}}
        403: {"success": false, "error": "error message", "data": {}}
        404: {"success": false, "error": "error message", "data": {}}
    """
    try:
        from app.validators import validate_email_format
        
        # Get email query parameter
        email = request.args.get('email')
        
        if not email:
            return jsonify({
                "success": False,
                "error": "Missing required query parameter: email",
                "data": {}
            }), 400
        
        # Validate email format
        is_valid, error_message = validate_email_format(email)
        if not is_valid:
            return jsonify({
                "success": False,
                "error": error_message,
                "data": {}
            }), 400
        
        # Check if workshop exists
        workshop_service, challenge_service, registration_service = get_services()
        workshop = workshop_service.get_workshop(workshop_id)
        
        if workshop is None:
            return jsonify({
                "success": False,
                "error": f"Workshop with ID '{workshop_id}' does not exist",
                "data": {}
            }), 404
        
        # Check if participant is registered
        registrations = registration_service.get_registrations_for_workshop(workshop_id)
        is_registered = any(r['participant_email'] == email for r in registrations)
        
        if not is_registered:
            return jsonify({
                "success": False,
                "error": "You must be registered to view challenges",
                "data": {}
            }), 403
        
        # Check workshop status
        status = workshop.get('status', 'pending')
        
        if status == 'pending':
            return jsonify({
                "success": False,
                "error": "Challenges are not available until the workshop begins",
                "data": {}
            }), 403
        elif status == 'completed':
            return jsonify({
                "success": False,
                "error": "Challenges are no longer available for completed workshops",
                "data": {}
            }), 403
        
        # Status is "ongoing" - return challenges
        challenges = challenge_service.get_challenges(workshop_id)
        
        return jsonify({
            "success": True,
            "data": challenges
        }), 200
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": "An unexpected error occurred. Please try again later.",
            "data": {}
        }), 500
