"""
Workshop Routes V2 - With Authentication and MySQL
"""
from flask import Blueprint, request, jsonify
from app.store.workshop_store_mysql import WorkshopStore
from app.auth.decorators import require_auth, optional_auth


# Create blueprint
workshop_bp_v2 = Blueprint('workshop_v2', __name__, url_prefix='/api')

# Initialize workshop store
workshop_store = WorkshopStore()


@workshop_bp_v2.route('/workshops', methods=['POST'])
@require_auth
def create_workshop():
    """
    Create a new workshop (requires authentication)
    
    POST /api/workshops
    
    Headers:
        Authorization: Bearer <access-token>
    
    Request Body:
    {
        "title": "Workshop Title",
        "description": "Workshop description"
    }
    
    Response (201):
    {
        "id": "uuid",
        "title": "Workshop Title",
        "description": "Workshop description",
        "status": "pending",
        "signup_enabled": true,
        "owner_id": "uuid",
        "created_at": "ISO-8601",
        "updated_at": "ISO-8601"
    }
    
    Errors:
    - 400: Invalid input
    - 401: Unauthorized
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
        
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        # Validate input
        if not title:
            return jsonify({
                "error": "Title is required",
                "code": "VALIDATION_ERROR",
                "status": 400
            }), 400
        
        if not description:
            return jsonify({
                "error": "Description is required",
                "code": "VALIDATION_ERROR",
                "status": 400
            }), 400
        
        if len(title) > 200:
            return jsonify({
                "error": "Title must not exceed 200 characters",
                "code": "VALIDATION_ERROR",
                "status": 400
            }), 400
        
        if len(description) > 1000:
            return jsonify({
                "error": "Description must not exceed 1000 characters",
                "code": "VALIDATION_ERROR",
                "status": 400
            }), 400
        
        # Get current user from request context (set by @require_auth)
        current_user = request.current_user
        
        # Create workshop
        workshop = workshop_store.create_workshop(
            title=title,
            description=description,
            owner_id=current_user['id']
        )
        
        return jsonify(workshop), 201
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@workshop_bp_v2.route('/workshops', methods=['GET'])
@optional_auth
def list_workshops():
    """
    List all workshops (authentication optional)
    
    GET /api/workshops
    
    Headers (optional):
        Authorization: Bearer <access-token>
    
    Response (200):
    [
        {
            "id": "uuid",
            "title": "Workshop Title",
            "description": "Workshop description",
            "status": "pending",
            "signup_enabled": true,
            "owner_id": "uuid",
            "created_at": "ISO-8601",
            "updated_at": "ISO-8601"
        }
    ]
    """
    try:
        workshops = workshop_store.get_all_workshops()
        return jsonify(workshops), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@workshop_bp_v2.route('/workshops/my', methods=['GET'])
@require_auth
def get_my_workshops():
    """
    Get workshops owned by current user
    
    GET /api/workshops/my
    
    Headers:
        Authorization: Bearer <access-token>
    
    Response (200):
    [
        {
            "id": "uuid",
            "title": "Workshop Title",
            "description": "Workshop description",
            "status": "pending",
            "signup_enabled": true,
            "owner_id": "uuid",
            "created_at": "ISO-8601",
            "updated_at": "ISO-8601"
        }
    ]
    
    Errors:
    - 401: Unauthorized
    - 500: Server error
    """
    try:
        # Get current user from request context
        current_user = request.current_user
        
        # Get workshops owned by user
        workshops = workshop_store.get_workshops_by_owner(current_user['id'])
        
        return jsonify(workshops), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@workshop_bp_v2.route('/workshops/<workshop_id>', methods=['GET'])
@optional_auth
def get_workshop(workshop_id):
    """
    Get workshop by ID (authentication optional)
    
    GET /api/workshops/<workshop_id>
    
    Headers (optional):
        Authorization: Bearer <access-token>
    
    Response (200):
    {
        "id": "uuid",
        "title": "Workshop Title",
        "description": "Workshop description",
        "status": "pending",
        "signup_enabled": true,
        "owner_id": "uuid",
        "created_at": "ISO-8601",
        "updated_at": "ISO-8601"
    }
    
    Errors:
    - 404: Workshop not found
    - 500: Server error
    """
    try:
        workshop = workshop_store.get_workshop_by_id(workshop_id)
        
        if not workshop:
            return jsonify({
                "error": "Workshop not found",
                "code": "WORKSHOP_NOT_FOUND",
                "status": 404
            }), 404
        
        return jsonify(workshop), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@workshop_bp_v2.route('/workshops/<workshop_id>', methods=['PATCH'])
@require_auth
def update_workshop(workshop_id):
    """
    Update workshop (owner only)
    
    PATCH /api/workshops/<workshop_id>
    
    Headers:
        Authorization: Bearer <access-token>
    
    Request Body (all fields optional):
    {
        "title": "New Title",
        "description": "New description",
        "status": "pending|ongoing|completed",
        "signup_enabled": true|false
    }
    
    Response (200):
    {
        "id": "uuid",
        "title": "Workshop Title",
        "description": "Workshop description",
        "status": "pending",
        "signup_enabled": true,
        "owner_id": "uuid",
        "created_at": "ISO-8601",
        "updated_at": "ISO-8601"
    }
    
    Errors:
    - 400: Invalid input
    - 401: Unauthorized
    - 403: Not workshop owner
    - 404: Workshop not found
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Get workshop
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
                "error": "Only the workshop owner can update this workshop",
                "code": "FORBIDDEN",
                "status": 403
            }), 403
        
        # Get request data
        data = request.get_json(silent=True)
        
        if not data:
            return jsonify({
                "error": "Request body is required",
                "code": "MISSING_BODY",
                "status": 400
            }), 400
        
        # Validate updates
        updates = {}
        
        if 'title' in data:
            title = data['title'].strip()
            if not title:
                return jsonify({
                    "error": "Title cannot be empty",
                    "code": "VALIDATION_ERROR",
                    "status": 400
                }), 400
            if len(title) > 200:
                return jsonify({
                    "error": "Title must not exceed 200 characters",
                    "code": "VALIDATION_ERROR",
                    "status": 400
                }), 400
            updates['title'] = title
        
        if 'description' in data:
            description = data['description'].strip()
            if not description:
                return jsonify({
                    "error": "Description cannot be empty",
                    "code": "VALIDATION_ERROR",
                    "status": 400
                }), 400
            if len(description) > 1000:
                return jsonify({
                    "error": "Description must not exceed 1000 characters",
                    "code": "VALIDATION_ERROR",
                    "status": 400
                }), 400
            updates['description'] = description
        
        if 'status' in data:
            status = data['status']
            if status not in ['pending', 'ongoing', 'completed']:
                return jsonify({
                    "error": "Status must be one of: pending, ongoing, completed",
                    "code": "VALIDATION_ERROR",
                    "status": 400
                }), 400
            updates['status'] = status
        
        if 'signup_enabled' in data:
            if not isinstance(data['signup_enabled'], bool):
                return jsonify({
                    "error": "signup_enabled must be a boolean",
                    "code": "VALIDATION_ERROR",
                    "status": 400
                }), 400
            updates['signup_enabled'] = data['signup_enabled']
        
        # Update workshop
        updated_workshop = workshop_store.update_workshop(workshop_id, updates)
        
        return jsonify(updated_workshop), 200
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500


@workshop_bp_v2.route('/workshops/<workshop_id>', methods=['DELETE'])
@require_auth
def delete_workshop(workshop_id):
    """
    Delete workshop (owner only)
    
    DELETE /api/workshops/<workshop_id>
    
    Headers:
        Authorization: Bearer <access-token>
    
    Response (204):
        No content
    
    Errors:
    - 401: Unauthorized
    - 403: Not workshop owner
    - 404: Workshop not found
    - 500: Server error
    """
    try:
        # Get current user
        current_user = request.current_user
        
        # Get workshop
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
                "error": "Only the workshop owner can delete this workshop",
                "code": "FORBIDDEN",
                "status": 403
            }), 403
        
        # Delete workshop
        workshop_store.delete_workshop(workshop_id)
        
        return '', 204
        
    except Exception as e:
        return jsonify({
            "error": "An unexpected error occurred",
            "code": "SERVER_ERROR",
            "status": 500
        }), 500
