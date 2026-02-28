"""
Participant Routes - Join Requests and Approval Workflow
"""
from flask import Blueprint, request, jsonify
from app.store.workshop_store_mysql import WorkshopStore
from app.store.participant_store import ParticipantStore
from app.auth.decorators import require_auth


# Create blueprint
participant_bp = Blueprint('participant', __name__, url_prefix='/api')

# Initialize stores
workshop_store = WorkshopStore()
participant_store = ParticipantStore()


@participant_bp.route('/workshops/<workshop_id>/join', methods=['POST'])
@require_auth
def join_workshop(workshop_id):
    """
    Join a workshop (create join request)
    
    POST /api/workshops/<workshop_id>/join
    
    Headers:
        Authorization: Bearer <access-token>
    
    Response (201):
    {
        "id": "uuid",
        "workshop_id": "uuid",
        "user_id": "uuid",
        "status": "pending",
        "requested_at": "ISO-8601",
        "approved_at": null,
        "approved_by": null,
        "user_name": "User Name",
        "user_email": "user@example.com"
    }
    
    Errors:
    - 400: Invalid request
    - 401: Unauthorized
    - 404: Workshop not found
    - 409: Already joined
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Check if workshop exists
        workshop = workshop_store.get_workshop_by_id(workshop_id)
        
        if not workshop:
            return jsonify({
                "error": "Workshop not found",
                "code": "WORKSHOP_NOT_FOUND",
                "status": 404
            }), 404
        
        # Check if user is the owner
        if workshop['owner_id'] == current_user['id']:
            return jsonify({
                "error": "Workshop owners cannot join their own workshops",
                "code": "OWNER_CANNOT_JOIN",
                "status": 400
            }), 400
        
        # Check if user already joined
        existing = participant_store.check_user_participation(workshop_id, current_user['id'])
        
        if existing:
            return jsonify({
                "error": f"You have already joined this workshop with status: {existing['status']}",
                "code": "ALREADY_JOINED",
                "status": 409
            }), 409
        
        # Create participant with pending status
        participant = participant_store.create_participant(
            workshop_id=workshop_id,
            user_id=current_user['id'],
            status='pending'
        )
        
        return jsonify(participant), 201
        
    except ValueError as e:
        return jsonify({
            "error": str(e),
            "code": "DUPLICATE_PARTICIPANT",
            "status": 409
        }), 409
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@participant_bp.route('/workshops/<workshop_id>/participants', methods=['GET'])
@require_auth
def get_workshop_participants(workshop_id):
    """
    Get participants for a workshop (owner only)
    
    GET /api/workshops/<workshop_id>/participants?status=pending
    
    Headers:
        Authorization: Bearer <access-token>
    
    Query Parameters:
        status: Optional filter (pending, joined, rejected, waitlisted)
    
    Response (200):
    {
        "pending": [...],
        "joined": [...],
        "rejected": [...],
        "waitlisted": [...]
    }
    
    Errors:
    - 401: Unauthorized
    - 403: Not workshop owner
    - 404: Workshop not found
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Check if workshop exists
        workshop = workshop_store.get_workshop_by_id(workshop_id)
        
        if not workshop:
            return jsonify({
                "error": "Workshop not found",
                "code": "WORKSHOP_NOT_FOUND",
                "status": 404
            }), 404
        
        # Check if user is owner
        if workshop['owner_id'] != current_user['id']:
            return jsonify({
                "error": "Only the workshop owner can view participants",
                "code": "FORBIDDEN",
                "status": 403
            }), 403
        
        # Get status filter from query params
        status_filter = request.args.get('status')
        
        if status_filter:
            # Return filtered list
            participants = participant_store.get_participants_by_workshop(workshop_id, status_filter)
            return jsonify(participants), 200
        else:
            # Return grouped by status
            all_participants = participant_store.get_participants_by_workshop(workshop_id)
            
            grouped = {
                'pending': [],
                'joined': [],
                'rejected': [],
                'waitlisted': []
            }
            
            for participant in all_participants:
                status = participant['status']
                if status in grouped:
                    grouped[status].append(participant)
            
            return jsonify(grouped), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@participant_bp.route('/workshops/<workshop_id>/participants/<participant_id>', methods=['PATCH'])
@require_auth
def update_participant_status(workshop_id, participant_id):
    """
    Update participant status (owner only)
    
    PATCH /api/workshops/<workshop_id>/participants/<participant_id>
    
    Headers:
        Authorization: Bearer <access-token>
    
    Request Body:
    {
        "status": "joined|rejected|waitlisted"
    }
    
    Response (200):
    {
        "id": "uuid",
        "workshop_id": "uuid",
        "user_id": "uuid",
        "status": "joined",
        "requested_at": "ISO-8601",
        "approved_at": "ISO-8601",
        "approved_by": "uuid",
        "user_name": "User Name",
        "user_email": "user@example.com"
    }
    
    Errors:
    - 400: Invalid status
    - 401: Unauthorized
    - 403: Not workshop owner
    - 404: Workshop or participant not found
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Check if workshop exists
        workshop = workshop_store.get_workshop_by_id(workshop_id)
        
        if not workshop:
            return jsonify({
                "error": "Workshop not found",
                "code": "WORKSHOP_NOT_FOUND",
                "status": 404
            }), 404
        
        # Check if user is owner
        if workshop['owner_id'] != current_user['id']:
            return jsonify({
                "error": "Only the workshop owner can update participant status",
                "code": "FORBIDDEN",
                "status": 403
            }), 403
        
        # Get participant
        participant = participant_store.get_participant_by_id(participant_id)
        
        if not participant:
            return jsonify({
                "error": "Participant not found",
                "code": "PARTICIPANT_NOT_FOUND",
                "status": 404
            }), 404
        
        # Verify participant belongs to this workshop
        if participant['workshop_id'] != workshop_id:
            return jsonify({
                "error": "Participant does not belong to this workshop",
                "code": "INVALID_PARTICIPANT",
                "status": 400
            }), 400
        
        # Get request data
        data = request.get_json(silent=True)
        
        if not data or 'status' not in data:
            return jsonify({
                "error": "Status is required",
                "code": "MISSING_STATUS",
                "status": 400
            }), 400
        
        new_status = data['status']
        
        # Validate status
        valid_statuses = ['pending', 'joined', 'rejected', 'waitlisted']
        if new_status not in valid_statuses:
            return jsonify({
                "error": f"Status must be one of: {', '.join(valid_statuses)}",
                "code": "INVALID_STATUS",
                "status": 400
            }), 400
        
        # Update participant status
        updated_participant = participant_store.update_participant_status(
            participant_id=participant_id,
            status=new_status,
            approved_by=current_user['id'] if new_status in ['joined', 'rejected'] else None
        )
        
        return jsonify(updated_participant), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@participant_bp.route('/workshops/<workshop_id>/participants/<participant_id>', methods=['DELETE'])
@require_auth
def remove_participant(workshop_id, participant_id):
    """
    Remove participant from workshop (owner or self)
    
    DELETE /api/workshops/<workshop_id>/participants/<participant_id>
    
    Headers:
        Authorization: Bearer <access-token>
    
    Response (204):
        No content
    
    Errors:
    - 401: Unauthorized
    - 403: Not authorized
    - 404: Workshop or participant not found
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Check if workshop exists
        workshop = workshop_store.get_workshop_by_id(workshop_id)
        
        if not workshop:
            return jsonify({
                "error": "Workshop not found",
                "code": "WORKSHOP_NOT_FOUND",
                "status": 404
            }), 404
        
        # Get participant
        participant = participant_store.get_participant_by_id(participant_id)
        
        if not participant:
            return jsonify({
                "error": "Participant not found",
                "code": "PARTICIPANT_NOT_FOUND",
                "status": 404
            }), 404
        
        # Verify participant belongs to this workshop
        if participant['workshop_id'] != workshop_id:
            return jsonify({
                "error": "Participant does not belong to this workshop",
                "code": "INVALID_PARTICIPANT",
                "status": 400
            }), 400
        
        # Check authorization: owner or self
        is_owner = workshop['owner_id'] == current_user['id']
        is_self = participant['user_id'] == current_user['id']
        
        if not (is_owner or is_self):
            return jsonify({
                "error": "Only the workshop owner or the participant can remove this participation",
                "code": "FORBIDDEN",
                "status": 403
            }), 403
        
        # Delete participant
        participant_store.delete_participant(participant_id)
        
        return '', 204
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@participant_bp.route('/workshops/joined', methods=['GET'])
@require_auth
def get_joined_workshops():
    """
    Get workshops the current user has joined
    
    GET /api/workshops/joined
    
    Headers:
        Authorization: Bearer <access-token>
    
    Response (200):
    [
        {
            "id": "uuid",
            "workshop_id": "uuid",
            "user_id": "uuid",
            "status": "joined",
            "requested_at": "ISO-8601",
            "approved_at": "ISO-8601",
            "approved_by": "uuid",
            "workshop_title": "Workshop Title",
            "workshop_description": "Description",
            "workshop_status": "ongoing",
            "workshop_owner_id": "uuid"
        }
    ]
    
    Errors:
    - 401: Unauthorized
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Get all participations for user
        participations = participant_store.get_participants_by_user(current_user['id'])
        
        return jsonify(participations), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500
