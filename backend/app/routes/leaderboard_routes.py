"""
Leaderboard Routes - API endpoints for points and rankings
"""
from flask import Blueprint, request, jsonify
from app.auth.decorators import require_auth, optional_auth
from app.store import points_store, workshop_store_mysql

leaderboard_bp = Blueprint('leaderboard', __name__)
workshop_store = workshop_store_mysql.WorkshopStore()


@leaderboard_bp.route('/leaderboard', methods=['GET'])
@optional_auth
def get_global_leaderboard(current_user):
    """Get global leaderboard"""
    limit = request.args.get('limit', 100, type=int)
    leaderboard = points_store.get_leaderboard(limit)
    
    # Add rank change info for each user
    for entry in leaderboard:
        rank_change = points_store.get_user_rank_change(entry['user_id'])
        entry['rank_info'] = rank_change
    
    # Add current user's position if authenticated
    response = {'leaderboard': leaderboard}
    
    if current_user:
        user_rank = points_store.get_user_rank_change(current_user['id'])
        response['current_user_rank'] = user_rank
    
    return jsonify(response), 200


@leaderboard_bp.route('/workshops/<workshop_id>/leaderboard', methods=['GET'])
def get_workshop_leaderboard(workshop_id):
    """Get leaderboard for a specific workshop"""
    workshop = workshop_store.get_workshop_by_id(workshop_id)
    if not workshop:
        return jsonify({'error': 'Workshop not found'}), 404
    
    leaderboard = points_store.get_workshop_leaderboard(workshop_id)
    
    return jsonify({
        'workshop_id': workshop_id,
        'workshop_title': workshop['title'],
        'leaderboard': leaderboard
    }), 200


@leaderboard_bp.route('/users/<user_id>/points', methods=['GET'])
def get_user_points(user_id):
    """Get points and stats for a user"""
    points = points_store.get_user_points(user_id)
    
    if not points:
        # Initialize if not exists
        points = points_store.initialize_user_points(user_id)
    
    rank_change = points_store.get_user_rank_change(user_id)
    
    return jsonify({
        'points': points,
        'rank_info': rank_change
    }), 200


@leaderboard_bp.route('/me/points', methods=['GET'])
@require_auth
def get_my_points(current_user):
    """Get current user's points and stats"""
    points = points_store.get_user_points(current_user['id'])
    
    if not points:
        # Initialize if not exists
        points = points_store.initialize_user_points(current_user['id'])
    
    rank_change = points_store.get_user_rank_change(current_user['id'])
    
    return jsonify({
        'points': points,
        'rank_info': rank_change
    }), 200


@leaderboard_bp.route('/leaderboard/update', methods=['POST'])
@require_auth
def update_leaderboard(current_user):
    """Manually trigger leaderboard update (admin/testing)"""
    points_store.update_rankings()
    return jsonify({'message': 'Leaderboard updated'}), 200
