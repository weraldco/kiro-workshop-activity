"""
Challenge Store - Data access layer for challenges and submissions
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from app.database.connection import get_db_cursor


def create_challenge(workshop_id: str, title: str, description: str,
                    html_content: str = None, solution: str = None,
                    order_index: int = 0, points: int = 20) -> Dict:
    """Create a new challenge"""
    challenge_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO challenges 
            (id, workshop_id, title, description, html_content, solution, order_index, points)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (challenge_id, workshop_id, title, description, html_content, solution, order_index, points))
        
        return get_challenge_by_id(challenge_id)


def get_challenge_by_id(challenge_id: str, include_solution: bool = False) -> Optional[Dict]:
    """Get challenge by ID"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM challenges WHERE id = %s
        """, (challenge_id,))
        challenge = cursor.fetchone()
        
        # Remove solution if not requested (for participants)
        if challenge and not include_solution:
            challenge.pop('solution', None)
        
        return challenge


def get_challenges_by_workshop(workshop_id: str, include_solution: bool = False) -> List[Dict]:
    """Get all challenges for a workshop"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM challenges 
            WHERE workshop_id = %s 
            ORDER BY order_index ASC, created_at ASC
        """, (workshop_id,))
        challenges = cursor.fetchall()
        
        # Remove solutions if not requested
        if not include_solution:
            for challenge in challenges:
                challenge.pop('solution', None)
        
        return challenges


def update_challenge(challenge_id: str, **kwargs) -> Optional[Dict]:
    """Update challenge fields"""
    allowed_fields = ['title', 'description', 'html_content', 'solution', 'order_index', 'points']
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return get_challenge_by_id(challenge_id, include_solution=True)
    
    set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [challenge_id]
    
    with get_db_cursor() as cursor:
        cursor.execute(f"""
            UPDATE challenges SET {set_clause} WHERE id = %s
        """, values)
        
        return get_challenge_by_id(challenge_id, include_solution=True)


def delete_challenge(challenge_id: str) -> bool:
    """Delete a challenge"""
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM challenges WHERE id = %s", (challenge_id,))
        return cursor.rowcount > 0


# Challenge Submissions
def submit_challenge(user_id: str, challenge_id: str, submission_text: str = None,
                    submission_url: str = None) -> Dict:
    """Submit a challenge solution"""
    submission_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        # Check if already submitted
        cursor.execute("""
            SELECT id FROM challenge_submissions 
            WHERE user_id = %s AND challenge_id = %s
        """, (user_id, challenge_id))
        
        existing = cursor.fetchone()
        if existing:
            # Update existing submission
            cursor.execute("""
                UPDATE challenge_submissions 
                SET submission_text = %s, submission_url = %s, 
                    status = 'pending', submitted_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (submission_text, submission_url, existing['id']))
            submission_id = existing['id']
        else:
            # Create new submission
            cursor.execute("""
                INSERT INTO challenge_submissions 
                (id, user_id, challenge_id, submission_text, submission_url, status)
                VALUES (%s, %s, %s, %s, %s, 'pending')
            """, (submission_id, user_id, challenge_id, submission_text, submission_url))
        
        cursor.execute("SELECT * FROM challenge_submissions WHERE id = %s", (submission_id,))
        return cursor.fetchone()


def get_submission(user_id: str, challenge_id: str) -> Optional[Dict]:
    """Get user's submission for a challenge"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM challenge_submissions 
            WHERE user_id = %s AND challenge_id = %s
        """, (user_id, challenge_id))
        return cursor.fetchone()


def get_submissions_by_challenge(challenge_id: str) -> List[Dict]:
    """Get all submissions for a challenge"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT cs.*, u.name as user_name, u.email as user_email
            FROM challenge_submissions cs
            JOIN users u ON cs.user_id = u.id
            WHERE cs.challenge_id = %s
            ORDER BY cs.submitted_at DESC
        """, (challenge_id,))
        return cursor.fetchall()


def review_submission(submission_id: str, reviewer_id: str, status: str,
                     points_earned: int, feedback: str = None) -> Dict:
    """Review a challenge submission"""
    with get_db_cursor() as cursor:
        cursor.execute("""
            UPDATE challenge_submissions 
            SET status = %s, points_earned = %s, feedback = %s,
                reviewed_by = %s, reviewed_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (status, points_earned, feedback, reviewer_id, submission_id))
        
        cursor.execute("SELECT * FROM challenge_submissions WHERE id = %s", (submission_id,))
        return cursor.fetchone()
