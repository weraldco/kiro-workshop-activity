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
            # Check if it's a capacity error (409) or other error
            if "full" in error.lower() or "capacity" in error.lower():
                return jsonify({
                    "success": False,
                    "error": error,
                    "data": {}
                }), 409
            else:
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
