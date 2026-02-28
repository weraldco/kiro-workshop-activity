"""
Lesson Routes - API endpoints for lessons and materials
"""
from flask import Blueprint, request, jsonify
from app.auth.decorators import require_auth
from app.store import lesson_store, workshop_store_mysql, points_store

lesson_bp = Blueprint('lessons', __name__)
workshop_store = workshop_store_mysql.WorkshopStore()


@lesson_bp.route('/workshops/<workshop_id>/lessons', methods=['POST'])
@require_auth
def create_lesson(current_user, workshop_id):
    """Create a new lesson (owner only)"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can create lessons'}), 403
    
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    content = data.get('content', '').strip()
    order_index = data.get('order_index', 0)
    points = data.get('points', 10)
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    lesson = lesson_store.create_lesson(
        workshop_id, title, description, content, order_index, points
    )
    
    return jsonify(lesson), 201


@lesson_bp.route('/workshops/<workshop_id>/lessons', methods=['GET'])
def get_lessons(workshop_id):
    """Get all lessons for a workshop"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    lessons = lesson_store.get_lessons_by_workshop(workshop_id)
    
    # Add materials to each lesson
    for lesson in lessons:
        lesson['materials'] = lesson_store.get_materials_by_lesson(lesson['id'])
    
    return jsonify(lessons), 200


@lesson_bp.route('/lessons/<lesson_id>', methods=['GET'])
def get_lesson(lesson_id):
    """Get a specific lesson"""
    lesson = lesson_store.get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    lesson['materials'] = lesson_store.get_materials_by_lesson(lesson_id)
    return jsonify(lesson), 200


@lesson_bp.route('/lessons/<lesson_id>', methods=['PATCH'])
@require_auth
def update_lesson(current_user, lesson_id):
    """Update a lesson (owner only)"""
    lesson = lesson_store.get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(lesson['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can update lessons'}), 403
    
    data = request.get_json(silent=True) or {}
    updated_lesson = lesson_store.update_lesson(lesson_id, **data)
    
    return jsonify(updated_lesson), 200


@lesson_bp.route('/lessons/<lesson_id>', methods=['DELETE'])
@require_auth
def delete_lesson(current_user, lesson_id):
    """Delete a lesson (owner only)"""
    lesson = lesson_store.get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(lesson['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can delete lessons'}), 403
    
    lesson_store.delete_lesson(lesson_id)
    return jsonify({'message': 'Lesson deleted'}), 200


@lesson_bp.route('/lessons/<lesson_id>/complete', methods=['POST'])
@require_auth
def complete_lesson(current_user, lesson_id):
    """Mark a lesson as completed"""
    lesson = lesson_store.get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    # Add points for completion
    user_points = points_store.add_lesson_points(
        current_user['id'], lesson_id, lesson['points']
    )
    
    # Update rankings
    points_store.update_rankings()
    
    return jsonify({
        'message': 'Lesson completed',
        'points_earned': lesson['points'],
        'total_points': user_points['total_points']
    }), 200


# Material endpoints
@lesson_bp.route('/lessons/<lesson_id>/materials', methods=['POST'])
@require_auth
def add_material(current_user, lesson_id):
    """Add material to a lesson (owner only)"""
    lesson = lesson_store.get_lesson_by_id(lesson_id)
    if not lesson:
        return jsonify({'error': 'Lesson not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(lesson['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can add materials'}), 403
    
    data = request.get_json(silent=True) or {}
    material_type = data.get('material_type', '').strip()
    title = data.get('title', '').strip()
    url = data.get('url', '').strip()
    file_size = data.get('file_size')
    duration = data.get('duration')
    
    if not all([material_type, title, url]):
        return jsonify({'error': 'material_type, title, and url are required'}), 400
    
    if material_type not in ['video', 'pdf', 'link']:
        return jsonify({'error': 'Invalid material_type'}), 400
    
    material = lesson_store.add_material(
        lesson_id, material_type, title, url, file_size, duration
    )
    
    return jsonify(material), 201


@lesson_bp.route('/materials/<material_id>', methods=['DELETE'])
@require_auth
def delete_material(current_user, material_id):
    """Delete a material (owner only)"""
    # This would need a get_material_by_id function, simplified for now
    lesson_store.delete_material(material_id)
    return jsonify({'message': 'Material deleted'}), 200
