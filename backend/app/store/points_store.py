"""
Points Store - Data access layer for user points and leaderboard
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from app.database.connection import get_db_cursor


def initialize_user_points(user_id: str) -> Dict:
    """Initialize points record for a user"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO user_points (user_id, total_points, lessons_completed, 
                                    challenges_completed, exams_passed)
            VALUES (%s, 0, 0, 0, 0)
            ON DUPLICATE KEY UPDATE user_id = user_id
        """, (user_id,))
        
        return get_user_points(user_id)


def get_user_points(user_id: str) -> Optional[Dict]:
    """Get points record for a user"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT up.*, u.name, u.email
            FROM user_points up
            JOIN users u ON up.user_id = u.id
            WHERE up.user_id = %s
        """, (user_id,))
        return cursor.fetchone()


def add_lesson_points(user_id: str, lesson_id: str, points: int) -> Dict:
    """Add points for completing a lesson"""
    progress_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        # Check if already completed
        cursor.execute("""
            SELECT id, completed FROM user_progress 
            WHERE user_id = %s AND lesson_id = %s
        """, (user_id, lesson_id))
        
        existing = cursor.fetchone()
        
        if existing and existing['completed']:
            # Already completed, don't add points again
            return get_user_points(user_id)
        
        if existing:
            # Mark as completed
            cursor.execute("""
                UPDATE user_progress 
                SET completed = TRUE, completed_at = CURRENT_TIMESTAMP, points_earned = %s
                WHERE id = %s
            """, (points, existing['id']))
        else:
            # Create new progress record
            cursor.execute("""
                INSERT INTO user_progress 
                (id, user_id, lesson_id, completed, completed_at, points_earned)
                VALUES (%s, %s, %s, TRUE, CURRENT_TIMESTAMP, %s)
            """, (progress_id, user_id, lesson_id, points))
        
        # Update user points
        cursor.execute("""
            INSERT INTO user_points (user_id, total_points, lessons_completed)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE 
                total_points = total_points + %s,
                lessons_completed = lessons_completed + 1
        """, (user_id, points, points))
        
        return get_user_points(user_id)


def add_challenge_points(user_id: str, challenge_id: str, points: int) -> Dict:
    """Add points for completing a challenge (called after review)"""
    with get_db_cursor() as cursor:
        # Update user points
        cursor.execute("""
            INSERT INTO user_points (user_id, total_points, challenges_completed)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE 
                total_points = total_points + %s,
                challenges_completed = challenges_completed + 1
        """, (user_id, points, points))
        
        return get_user_points(user_id)


def add_exam_points(user_id: str, exam_id: str, points: int) -> Dict:
    """Add points for passing an exam"""
    with get_db_cursor() as cursor:
        # Check if already passed this exam
        cursor.execute("""
            SELECT COUNT(*) as count FROM exam_attempts 
            WHERE user_id = %s AND exam_id = %s AND passed = TRUE
        """, (user_id, exam_id))
        
        result = cursor.fetchone()
        if result['count'] > 1:
            # Already passed before, don't add points again
            return get_user_points(user_id)
        
        # Update user points
        cursor.execute("""
            INSERT INTO user_points (user_id, total_points, exams_passed)
            VALUES (%s, %s, 1)
            ON DUPLICATE KEY UPDATE 
                total_points = total_points + %s,
                exams_passed = exams_passed + 1
        """, (user_id, points, points))
        
        return get_user_points(user_id)


def get_leaderboard(limit: int = 100) -> List[Dict]:
    """Get global leaderboard"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT up.*, u.name, u.email
            FROM user_points up
            JOIN users u ON up.user_id = u.id
            WHERE up.total_points > 0
            ORDER BY up.total_points DESC, up.last_updated ASC
            LIMIT %s
        """, (limit,))
        return cursor.fetchall()


def update_rankings() -> None:
    """Update all user rankings and track changes"""
    with get_db_cursor() as cursor:
        # Get current rankings
        cursor.execute("""
            SELECT user_id, total_points,
                   ROW_NUMBER() OVER (ORDER BY total_points DESC, last_updated ASC) as new_rank
            FROM user_points
            WHERE total_points > 0
        """)
        rankings = cursor.fetchall()
        
        for rank_data in rankings:
            user_id = rank_data['user_id']
            new_rank = rank_data['new_rank']
            total_points = rank_data['total_points']
            
            # Get current rank
            cursor.execute("""
                SELECT current_rank FROM user_points WHERE user_id = %s
            """, (user_id,))
            current = cursor.fetchone()
            current_rank = current['current_rank'] if current else 0
            
            # Update ranks
            cursor.execute("""
                UPDATE user_points 
                SET previous_rank = current_rank, current_rank = %s
                WHERE user_id = %s
            """, (new_rank, user_id))
            
            # Record in history if rank changed
            if current_rank != new_rank:
                history_id = str(uuid.uuid4())
                cursor.execute("""
                    INSERT INTO leaderboard_history 
                    (id, user_id, rank_position, total_points)
                    VALUES (%s, %s, %s, %s)
                """, (history_id, user_id, new_rank, total_points))


def get_user_rank_change(user_id: str) -> Dict:
    """Get user's rank change (up/down/same)"""
    points = get_user_points(user_id)
    
    if not points:
        return {'rank': 0, 'change': 0, 'direction': 'same'}
    
    current_rank = points.get('current_rank', 0)
    previous_rank = points.get('previous_rank', 0)
    
    if previous_rank == 0:
        change = 0
        direction = 'new'
    elif current_rank < previous_rank:
        change = previous_rank - current_rank
        direction = 'up'
    elif current_rank > previous_rank:
        change = current_rank - previous_rank
        direction = 'down'
    else:
        change = 0
        direction = 'same'
    
    return {
        'rank': current_rank,
        'previous_rank': previous_rank,
        'change': change,
        'direction': direction,
        'total_points': points.get('total_points', 0)
    }


def get_workshop_leaderboard(workshop_id: str) -> List[Dict]:
    """Get leaderboard for a specific workshop"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT 
                u.id as user_id,
                u.name,
                u.email,
                COALESCE(SUM(up.points_earned), 0) + 
                COALESCE(SUM(cs.points_earned), 0) + 
                COALESCE(SUM(ea.points_earned), 0) as total_points,
                COUNT(DISTINCT CASE WHEN up.completed THEN up.lesson_id END) as lessons_completed,
                COUNT(DISTINCT CASE WHEN cs.status = 'passed' THEN cs.challenge_id END) as challenges_completed,
                COUNT(DISTINCT CASE WHEN ea.passed THEN ea.exam_id END) as exams_passed
            FROM participants p
            JOIN users u ON p.user_id = u.id
            LEFT JOIN user_progress up ON up.user_id = u.id 
                AND up.lesson_id IN (SELECT id FROM lessons WHERE workshop_id = %s)
            LEFT JOIN challenge_submissions cs ON cs.user_id = u.id 
                AND cs.challenge_id IN (SELECT id FROM challenges WHERE workshop_id = %s)
            LEFT JOIN exam_attempts ea ON ea.user_id = u.id 
                AND ea.exam_id IN (SELECT id FROM exams WHERE workshop_id = %s)
            WHERE p.workshop_id = %s AND p.status = 'joined'
            GROUP BY u.id, u.name, u.email
            ORDER BY total_points DESC
        """, (workshop_id, workshop_id, workshop_id, workshop_id))
        return cursor.fetchall()
