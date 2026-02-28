"""
Exam Routes - API endpoints for exams and attempts
"""
from flask import Blueprint, request, jsonify
from app.auth.decorators import require_auth
from app.store import exam_store, workshop_store_mysql, points_store, participant_store

exam_bp = Blueprint('exams', __name__)
workshop_store = workshop_store_mysql.WorkshopStore()


@exam_bp.route('/workshops/<workshop_id>/exams', methods=['POST'])
@require_auth
def create_exam(current_user, workshop_id):
    """Create a new exam (owner only)"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can create exams'}), 403
    
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    duration_minutes = data.get('duration_minutes', 60)
    passing_score = data.get('passing_score', 70)
    points = data.get('points', 50)
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    exam = exam_store.create_exam(
        workshop_id, title, description, duration_minutes, passing_score, points
    )
    
    return jsonify(exam), 201


@exam_bp.route('/workshops/<workshop_id>/exams', methods=['GET'])
def get_exams(workshop_id):
    """Get all exams for a workshop"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    exams = exam_store.get_exams_by_workshop(workshop_id)
    return jsonify(exams), 200


@exam_bp.route('/exams/<exam_id>', methods=['GET'])
@require_auth
def get_exam(current_user, exam_id):
    """Get exam details with questions"""
    exam = exam_store.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(exam['workshop_id'])
    is_owner = workshop['owner_id'] == current_user['id']
    
    # Get questions (with or without answers)
    exam['questions'] = exam_store.get_questions_by_exam(exam_id, include_answers=is_owner)
    
    # Get user's best attempt if participant
    if not is_owner:
        best_attempt = exam_store.get_best_attempt(current_user['id'], exam_id)
        exam['best_attempt'] = best_attempt
    
    return jsonify(exam), 200


@exam_bp.route('/exams/<exam_id>', methods=['PATCH'])
@require_auth
def update_exam(current_user, exam_id):
    """Update an exam (owner only)"""
    exam = exam_store.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(exam['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can update exams'}), 403
    
    data = request.get_json(silent=True) or {}
    updated_exam = exam_store.update_exam(exam_id, **data)
    
    return jsonify(updated_exam), 200


@exam_bp.route('/exams/<exam_id>', methods=['DELETE'])
@require_auth
def delete_exam(current_user, exam_id):
    """Delete an exam (owner only)"""
    exam = exam_store.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(exam['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can delete exams'}), 403
    
    exam_store.delete_exam(exam_id)
    return jsonify({'message': 'Exam deleted'}), 200


# Question endpoints
@exam_bp.route('/exams/<exam_id>/questions', methods=['POST'])
@require_auth
def add_question(current_user, exam_id):
    """Add a question to an exam (owner only)"""
    exam = exam_store.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(exam['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can add questions'}), 403
    
    data = request.get_json(silent=True) or {}
    question_text = data.get('question_text', '').strip()
    question_type = data.get('question_type', 'multiple_choice')
    correct_answer = data.get('correct_answer', '').strip()
    options = data.get('options', [])
    points = data.get('points', 10)
    order_index = data.get('order_index', 0)
    
    if not question_text or not correct_answer:
        return jsonify({'error': 'question_text and correct_answer are required'}), 400
    
    question = exam_store.add_question(
        exam_id, question_text, question_type, correct_answer, options, points, order_index
    )
    
    return jsonify(question), 201


@exam_bp.route('/questions/<question_id>', methods=['PATCH'])
@require_auth
def update_question(current_user, question_id):
    """Update a question (owner only)"""
    data = request.get_json(silent=True) or {}
    updated_question = exam_store.update_question(question_id, **data)
    
    return jsonify(updated_question), 200


@exam_bp.route('/questions/<question_id>', methods=['DELETE'])
@require_auth
def delete_question(current_user, question_id):
    """Delete a question (owner only)"""
    exam_store.delete_question(question_id)
    return jsonify({'message': 'Question deleted'}), 200


# Attempt endpoints
@exam_bp.route('/exams/<exam_id>/start', methods=['POST'])
@require_auth
def start_attempt(current_user, exam_id):
    """Start an exam attempt"""
    exam = exam_store.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    # Check if user is participant
    participation = participant_store.get_participation(
        exam['workshop_id'], current_user['id']
    )
    if not participation or participation['status'] != 'joined':
        return jsonify({'error': 'Must be a joined participant to take exam'}), 403
    
    attempt = exam_store.start_exam_attempt(current_user['id'], exam_id)
    
    # Include questions without answers
    exam['questions'] = exam_store.get_questions_by_exam(exam_id, include_answers=False)
    attempt['exam'] = exam
    
    return jsonify(attempt), 201


@exam_bp.route('/attempts/<attempt_id>/submit', methods=['POST'])
@require_auth
def submit_attempt(current_user, attempt_id):
    """Submit exam answers"""
    data = request.get_json(silent=True) or {}
    answers = data.get('answers', {})
    
    if not answers:
        return jsonify({'error': 'Answers are required'}), 400
    
    attempt = exam_store.submit_exam_attempt(attempt_id, answers)
    
    # Add points if passed
    if attempt['passed'] and attempt['points_earned'] > 0:
        points_store.add_exam_points(
            current_user['id'], attempt['exam_id'], attempt['points_earned']
        )
        points_store.update_rankings()
    
    return jsonify(attempt), 200


@exam_bp.route('/exams/<exam_id>/attempts', methods=['GET'])
@require_auth
def get_attempts(current_user, exam_id):
    """Get user's attempts for an exam"""
    exam = exam_store.get_exam_by_id(exam_id)
    if not exam:
        return jsonify({'error': 'Exam not found'}), 404
    
    attempts = exam_store.get_user_exam_attempts(current_user['id'], exam_id)
    return jsonify(attempts), 200
