"""
Lesson Store - Data access layer for lessons and materials
"""
import uuid
from datetime import datetime
from typing import List, Dict, Optional
from app.database.connection import get_db_cursor


def create_lesson(workshop_id: str, title: str, description: str = None, 
                 content: str = None, order_index: int = 0, points: int = 10) -> Dict:
    """Create a new lesson"""
    lesson_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO lessons (id, workshop_id, title, description, content, order_index, points)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (lesson_id, workshop_id, title, description, content, order_index, points))
        
        return get_lesson_by_id(lesson_id)


def get_lesson_by_id(lesson_id: str) -> Optional[Dict]:
    """Get lesson by ID"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM lessons WHERE id = %s
        """, (lesson_id,))
        return cursor.fetchone()


def get_lessons_by_workshop(workshop_id: str) -> List[Dict]:
    """Get all lessons for a workshop"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM lessons 
            WHERE workshop_id = %s 
            ORDER BY order_index ASC, created_at ASC
        """, (workshop_id,))
        return cursor.fetchall()


def update_lesson(lesson_id: str, **kwargs) -> Optional[Dict]:
    """Update lesson fields"""
    allowed_fields = ['title', 'description', 'content', 'order_index', 'points']
    updates = {k: v for k, v in kwargs.items() if k in allowed_fields}
    
    if not updates:
        return get_lesson_by_id(lesson_id)
    
    set_clause = ', '.join([f"{k} = %s" for k in updates.keys()])
    values = list(updates.values()) + [lesson_id]
    
    with get_db_cursor() as cursor:
        cursor.execute(f"""
            UPDATE lessons SET {set_clause} WHERE id = %s
        """, values)
        
        return get_lesson_by_id(lesson_id)


def delete_lesson(lesson_id: str) -> bool:
    """Delete a lesson"""
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM lessons WHERE id = %s", (lesson_id,))
        return cursor.rowcount > 0


# Lesson Materials
def add_material(lesson_id: str, material_type: str, title: str, url: str,
                file_size: int = None, duration: int = None) -> Dict:
    """Add material to a lesson"""
    material_id = str(uuid.uuid4())
    
    with get_db_cursor() as cursor:
        cursor.execute("""
            INSERT INTO lesson_materials 
            (id, lesson_id, material_type, title, url, file_size, duration)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (material_id, lesson_id, material_type, title, url, file_size, duration))
        
        cursor.execute("SELECT * FROM lesson_materials WHERE id = %s", (material_id,))
        return cursor.fetchone()


def get_materials_by_lesson(lesson_id: str) -> List[Dict]:
    """Get all materials for a lesson"""
    with get_db_cursor(commit=False) as cursor:
        cursor.execute("""
            SELECT * FROM lesson_materials 
            WHERE lesson_id = %s 
            ORDER BY created_at ASC
        """, (lesson_id,))
        return cursor.fetchall()


def delete_material(material_id: str) -> bool:
    """Delete a material"""
    with get_db_cursor() as cursor:
        cursor.execute("DELETE FROM lesson_materials WHERE id = %s", (material_id,))
        return cursor.rowcount > 0
