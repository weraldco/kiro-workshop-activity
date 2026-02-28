"""
Challenge Routes - API endpoints for challenges and submissions
"""
from flask import Blueprint, request, jsonify
from app.auth.decorators import require_auth
from app.store import challenge_store, workshop_store_mysql, points_store, participant_store

challenge_bp = Blueprint('challenges', __name__)
workshop_store = workshop_store_mysql.WorkshopStore()


@challenge_bp.route('/workshops/<workshop_id>/challenges', methods=['POST'])
@require_auth
def create_challenge(current_user, workshop_id):
    """Create a new challenge (owner only)"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can create challenges'}), 403
    
    data = request.get_json(silent=True) or {}
    title = data.get('title', '').strip()
    description = data.get('description', '').strip()
    html_content = data.get('html_content', '').strip()
    solution = data.get('solution', '').strip()
    order_index = data.get('order_index', 0)
    points = data.get('points', 20)
    
    if not title or not description:
        return jsonify({'error': 'Title and description are required'}), 400
    
    challenge = challenge_store.create_challenge(
        workshop_id, title, description, html_content, solution, order_index, points
    )
    
    return jsonify(challenge), 201


@challenge_bp.route('/workshops/<workshop_id>/challenges', methods=['GET'])
@require_auth
def get_challenges(current_user, workshop_id):
    """Get all challenges for a workshop"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    # Check if user is owner (can see solutions)
    is_owner = workshop['owner_id'] == current_user['id']
    
    challenges = challenge_store.get_challenges_by_workshop(workshop_id, include_solution=is_owner)
    
    # Add submission status for participant
    if not is_owner:
        for challenge in challenges:
            submission = challenge_store.get_submission(current_user['id'], challenge['id'])
            challenge['submission'] = submission
    
    return jsonify(challenges), 200


@challenge_bp.route('/challenges/<challenge_id>', methods=['GET'])
@require_auth
def get_challenge(current_user, challenge_id):
    """Get a specific challenge"""
    challenge = challenge_store.get_challenge_by_id(challenge_id, include_solution=False)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(challenge['workshop_id'])
    
    # Include solution if owner
    if workshop['owner_id'] == current_user['id']:
        challenge = challenge_store.get_challenge_by_id(challenge_id, include_solution=True)
    else:
        # Include submission for participant
        submission = challenge_store.get_submission(current_user['id'], challenge_id)
        challenge['submission'] = submission
    
    return jsonify(challenge), 200


@challenge_bp.route('/challenges/<challenge_id>', methods=['PATCH'])
@require_auth
def update_challenge(current_user, challenge_id):
    """Update a challenge (owner only)"""
    challenge = challenge_store.get_challenge_by_id(challenge_id, include_solution=True)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(challenge['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can update challenges'}), 403
    
    data = request.get_json(silent=True) or {}
    updated_challenge = challenge_store.update_challenge(challenge_id, **data)
    
    return jsonify(updated_challenge), 200


@challenge_bp.route('/challenges/<challenge_id>', methods=['DELETE'])
@require_auth
def delete_challenge(current_user, challenge_id):
    """Delete a challenge (owner only)"""
    challenge = challenge_store.get_challenge_by_id(challenge_id, include_solution=True)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(challenge['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can delete challenges'}), 403
    
    challenge_store.delete_challenge(challenge_id)
    return jsonify({'message': 'Challenge deleted'}), 200


# Submission endpoints
@challenge_bp.route('/challenges/<challenge_id>/submit', methods=['POST'])
@require_auth
def submit_challenge(current_user, challenge_id):
    """Submit a challenge solution"""
    challenge = challenge_store.get_challenge_by_id(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    # Check if user is participant
    participation = participant_store.get_participation(
        challenge['workshop_id'], current_user['id']
    )
    if not participation or participation['status'] != 'joined':
        return jsonify({'error': 'Must be a joined participant to submit'}), 403
    
    data = request.get_json(silent=True) or {}
    submission_text = data.get('submission_text', '').strip()
    submission_url = data.get('submission_url', '').strip()
    
    if not submission_text and not submission_url:
        return jsonify({'error': 'Either submission_text or submission_url is required'}), 400
    
    submission = challenge_store.submit_challenge(
        current_user['id'], challenge_id, submission_text, submission_url
    )
    
    return jsonify(submission), 201


@challenge_bp.route('/challenges/<challenge_id>/submissions', methods=['GET'])
@require_auth
def get_submissions(current_user, challenge_id):
    """Get all submissions for a challenge (owner only)"""
    challenge = challenge_store.get_challenge_by_id(challenge_id)
    if not challenge:
        return jsonify({'error': 'Challenge not found'}), 404
    
    workshop = workshop_store.get_workshop_by_id(challenge['workshop_id'])
    if workshop['owner_id'] != current_user['id']:
        return jsonify({'error': 'Only workshop owner can view submissions'}), 403
    
    submissions = challenge_store.get_submissions_by_challenge(challenge_id)
    return jsonify(submissions), 200


@challenge_bp.route('/submissions/<submission_id>/review', methods=['POST'])
@require_auth
def review_submission(current_user, submission_id):
    """Review a challenge submission (owner only)"""
    data = request.get_json(silent=True) or {}
    status = data.get('status', '').strip()
    points_earned = data.get('points_earned', 0)
    feedback = data.get('feedback', '').strip()
    
    if status not in ['passed', 'failed']:
        return jsonify({'error': 'Status must be passed or failed'}), 400
    
    submission = challenge_store.review_submission(
        submission_id, current_user['id'], status, points_earned, feedback
    )
    
    # Add points if passed
    if status == 'passed' and points_earned > 0:
        points_store.add_challenge_points(
            submission['user_id'], submission['challenge_id'], points_earned
        )
        points_store.update_rankings()
    
    return jsonify(submission), 200
