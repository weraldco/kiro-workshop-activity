"""
Exam Store - Data access layer for exams and attempts
"""
import uuid
import json
from datetime import datetime
from typing import List, Dict, Optional
from app.database.connection import get_db_cursor


def create_exam(workshop_id: str, title: str, description: str = None,
               duration_minutes: int = 60, passing_score: int = 70, points: int = 50) -> Dict:
    """Create a new exam"""
    exam_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO exams 
            (id, workshop_id, title, description, duration_minutes, passing_score, points)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (exam_id, workshop_id, title, description, duration_minutes, passing_score, points))
        
        return get_exam_by_id(exam_id)


def get_exam_by_id(exam_id: str) -> Optional[Dict]:
    """Get exam by ID"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("SELECT * FROM exams WHERE id = %s", (exam_id,))
        return cursor.fetchone()


def get_exams_by_workshop(workshop_id: str) -> List[Dict]:
    """Get all exams for a workshop"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM exams 
            WHERE workshop_id = %s 
            ORDER BY created_at ASC
        """, (workshop_id,))
        return cursor.fetchall()


def update_exam(exam_id: str, **kwargs) -> Optional[Dict]:
    """Update exam fields"""
    allowed_fields = ['title', 'description', 'duration_minutes', 'passing_score', 'points']
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return get_exam_by_id(exam_id)
    
    set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [exam_id]
    
    with get_db_cursor() as cursor:
        cursor.execute(f"UPDATE exams SET {set_clause} WHERE id = %s", values)
        return get_exam_by_id(exam_id)


def delete_exam(exam_id: str) -> bool:
    """Delete an exam"""
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM exams WHERE id = %s", (exam_id,))
        return cursor.rowcount > 0


# Exam Questions
def add_question(exam_id: str, question_text: str, question_type: str,
                correct_answer: str, options: List[str] = None, 
                points: int = 10, order_index: int = 0) -> Dict:
    """Add a question to an exam"""
    question_id = str(uuid.uuid4())
    options_json = json.dumps(options) if options else None
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO exam_questions 
            (id, exam_id, question_text, question_type, options, correct_answer, points, order_index)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (question_id, exam_id, question_text, question_type, options_json, 
              correct_answer, points, order_index))
        
        cursor.execute("SELECT * FROM exam_questions WHERE id = %s", (question_id,))
        question = cursor.fetchone()
        
        # Parse JSON options
        if question and question.get('options'):
            question['options'] = json.loads(question['options'])
        
        return question


def get_questions_by_exam(exam_id: str, include_answers: bool = False) -> List[Dict]:
    """Get all questions for an exam"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM exam_questions 
            WHERE exam_id = %s 
            ORDER BY order_index ASC, created_at ASC
        """, (exam_id,))
        questions = cursor.fetchall()
        
        for question in questions:
            # Parse JSON options
            if question.get('options'):
                question['options'] = json.loads(question['options'])
            
            # Remove correct answer if not requested (for participants)
            if not include_answers:
                question.pop('correct_answer', None)
        
        return questions


def update_question(question_id: str, **kwargs) -> Optional[Dict]:
    """Update question fields"""
    allowed_fields = ['question_text', 'question_type', 'options', 'correct_answer', 'points', 'order_index']
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("SELECT * FROM exam_questions WHERE id = %s", (question_id,))
            return cursor.fetchone()
    
    # Convert options list to JSON
    if 'options' in updates and isinstance(updates['options'], list):
        updates['options'] = json.dumps(updates['options'])
    
    set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [question_id]
    
    with get_db_cursor() as cursor:
        cursor.execute(f"UPDATE exam_questions SET {set_clause} WHERE id = %s", values)
        cursor.execute("SELECT * FROM exam_questions WHERE id = %s", (question_id,))
        return cursor.fetchone()


def delete_question(question_id: str) -> bool:
    """Delete a question"""
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM exam_questions WHERE id = %s", (question_id,))
        return cursor.rowcount > 0


# Exam Attempts
def start_exam_attempt(user_id: str, exam_id: str) -> Dict:
    """Start an exam attempt"""
    attempt_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO exam_attempts (id, user_id, exam_id, answers)
            VALUES (%s, %s, %s, %s)
        """, (attempt_id, user_id, exam_id, json.dumps({})))
        
        cursor.execute("SELECT * FROM exam_attempts WHERE id = %s", (attempt_id,))
        attempt = cursor.fetchone()
        
        if attempt and attempt.get('answers'):
            attempt['answers'] = json.loads(attempt['answers'])
        
        return attempt


def submit_exam_attempt(attempt_id: str, answers: Dict) -> Dict:
    """Submit exam answers and calculate score"""
    with get_db_cursor() as cursor:
        # Get the exam and questions
        cursor.execute("""
            SELECT ea.exam_id, e.passing_score, e.points
            FROM exam_attempts ea
            JOIN exams e ON ea.exam_id = e.id
            WHERE ea.id = %s
        """, (attempt_id,))
        
        attempt_info = cursor.fetchone()
        if not attempt_info:
            raise ValueError("Exam attempt not found")
        
        exam_id = attempt_info['exam_id']
        passing_score = attempt_info['passing_score']
        max_points = attempt_info['points']
        
        # Get questions with correct answers
        cursor.execute("""
            SELECT id, correct_answer, points 
            FROM exam_questions 
            WHERE exam_id = %s
        """, (exam_id,))
        questions = cursor.fetchall()
        
        # Calculate score
        total_possible = sum(q['points'] for q in questions)
        earned_points = 0
        
        for question in questions:
            user_answer = answers.get(question['id'], '')
            if str(user_answer).strip().lower() == str(question['correct_answer']).strip().lower():
                earned_points += question['points']
        
        score = int((earned_points / total_possible * 100)) if total_possible > 0 else 0
        passed = score >= passing_score
        points_earned = max_points if passed else 0
        
        # Update attempt
        cursor.execute("""
            UPDATE exam_attempts 
            SET answers = %s, score = %s, points_earned = %s, 
                passed = %s, submitted_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (json.dumps(answers), score, points_earned, passed, attempt_id))
        
        cursor.execute("SELECT * FROM exam_attempts WHERE id = %s", (attempt_id,))
        attempt = cursor.fetchone()
        
        if attempt and attempt.get('answers'):
            attempt['answers'] = json.loads(attempt['answers'])
        
        return attempt


def get_user_exam_attempts(user_id: str, exam_id: str) -> List[Dict]:
    """Get all attempts by a user for an exam"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM exam_attempts 
            WHERE user_id = %s AND exam_id = %s
            ORDER BY started_at DESC
        """, (user_id, exam_id))
        attempts = cursor.fetchall()
        
        for attempt in attempts:
            if attempt.get('answers'):
                attempt['answers'] = json.loads(attempt['answers'])
        
        return attempts


def get_best_attempt(user_id: str, exam_id: str) -> Optional[Dict]:
    """Get user's best attempt for an exam"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM exam_attempts 
            WHERE user_id = %s AND exam_id = %s AND submitted_at IS NOT NULL
            ORDER BY score DESC, submitted_at ASC
            LIMIT 1
        """, (user_id, exam_id))
        attempt = cursor.fetchone()
        
        if attempt and attempt.get('answers'):
            attempt['answers'] = json.loads(attempt['answers'])
        
        return attempt
