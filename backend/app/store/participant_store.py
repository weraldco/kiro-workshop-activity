"""
Participant Store - MySQL Implementation
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any, List
from app.database.connection import get_db_cursor
from mysql.connector import Error, IntegrityError


class ParticipantStore:
    """Manages participant data persistence using MySQL"""
    
    def __init__(self):
        """Initialize ParticipantStore"""
        pass
    
    def create_participant(
        self, 
        workshop_id: str, 
        user_id: str, 
        status: str = 'pending'
    ) -> Optional[Dict[str, Any]]:
        """
        Create a new participant (join request)
        
        Args:
            workshop_id: Workshop ID
            user_id: User ID
            status: Participant status (pending, joined, rejected, waitlisted)
            
        Returns:
            Created participant dict or None if duplicate
            
        Raises:
            ValueError: If user already joined this workshop
        """
        participant_id = str(uuid.uuid4())
        
        try:
            with get_db_cursor() as cursor:
                cursor.execute("""
                    INSERT INTO participants (id, workshop_id, user_id, status)
                    VALUES (%s, %s, %s, %s)
                """, (participant_id, workshop_id, user_id, status))
                
                # Fetch the created participant with user info
                cursor.execute("""
                    SELECT p.id, p.workshop_id, p.user_id, p.status,
                           p.requested_at, p.approved_at, p.approved_by,
                           u.name as user_name, u.email as user_email
                    FROM participants p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.id = %s
                """, (participant_id,))
                
                participant = cursor.fetchone()
                
                if participant:
                    # Convert datetime to ISO string
                    participant['requested_at'] = participant['requested_at'].isoformat() if participant['requested_at'] else None
                    participant['approved_at'] = participant['approved_at'].isoformat() if participant['approved_at'] else None
                
                return participant
                
        except IntegrityError as e:
            # Duplicate entry (user already joined this workshop)
            if 'unique_workshop_user' in str(e).lower() or 'duplicate' in str(e).lower():
                raise ValueError(f"User already joined this workshop")
            raise
    
    def get_participant_by_id(self, participant_id: str) -> Optional[Dict[str, Any]]:
        """
        Get participant by ID
        
        Args:
            participant_id: Participant ID
            
        Returns:
            Participant dict or None if not found
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT p.id, p.workshop_id, p.user_id, p.status,
                       p.requested_at, p.approved_at, p.approved_by,
                       u.name as user_name, u.email as user_email
                FROM participants p
                JOIN users u ON p.user_id = u.id
                WHERE p.id = %s
            """, (participant_id,))
            
            participant = cursor.fetchone()
            
            if participant:
                # Convert datetime to ISO string
                participant['requested_at'] = participant['requested_at'].isoformat() if participant['requested_at'] else None
                participant['approved_at'] = participant['approved_at'].isoformat() if participant['approved_at'] else None
            
            return participant
    
    def get_participants_by_workshop(
        self, 
        workshop_id: str, 
        status: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get all participants for a workshop, optionally filtered by status
        
        Args:
            workshop_id: Workshop ID
            status: Optional status filter (pending, joined, rejected, waitlisted)
            
        Returns:
            List of participant dicts
        """
        with get_db_cursor(commit=False) as cursor:
            if status:
                cursor.execute("""
                    SELECT p.id, p.workshop_id, p.user_id, p.status,
                           p.requested_at, p.approved_at, p.approved_by,
                           u.name as user_name, u.email as user_email
                    FROM participants p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.workshop_id = %s AND p.status = %s
                    ORDER BY p.requested_at DESC
                """, (workshop_id, status))
            else:
                cursor.execute("""
                    SELECT p.id, p.workshop_id, p.user_id, p.status,
                           p.requested_at, p.approved_at, p.approved_by,
                           u.name as user_name, u.email as user_email
                    FROM participants p
                    JOIN users u ON p.user_id = u.id
                    WHERE p.workshop_id = %s
                    ORDER BY p.requested_at DESC
                """, (workshop_id,))
            
            participants = cursor.fetchall()
            
            # Convert datetime fields
            for participant in participants:
                participant['requested_at'] = participant['requested_at'].isoformat() if participant['requested_at'] else None
                participant['approved_at'] = participant['approved_at'].isoformat() if participant['approved_at'] else None
            
            return participants
    
    def get_participants_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get all workshops a user has joined (any status)
        
        Args:
            user_id: User ID
            
        Returns:
            List of participant dicts with workshop info
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT p.id, p.workshop_id, p.user_id, p.status,
                       p.requested_at, p.approved_at, p.approved_by,
                       w.title as workshop_title, w.description as workshop_description,
                       w.status as workshop_status, w.owner_id as workshop_owner_id
                FROM participants p
                JOIN workshops w ON p.workshop_id = w.id
                WHERE p.user_id = %s
                ORDER BY p.requested_at DESC
            """, (user_id,))
            
            participants = cursor.fetchall()
            
            # Convert datetime fields
            for participant in participants:
                participant['requested_at'] = participant['requested_at'].isoformat() if participant['requested_at'] else None
                participant['approved_at'] = participant['approved_at'].isoformat() if participant['approved_at'] else None
            
            return participants
    
    def check_user_participation(self, workshop_id: str, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Check if user has already joined a workshop
        
        Args:
            workshop_id: Workshop ID
            user_id: User ID
            
        Returns:
            Participant dict if exists, None otherwise
        """
        with get_db_cursor(commit=False) as cursor:
            cursor.execute("""
                SELECT p.id, p.workshop_id, p.user_id, p.status,
                       p.requested_at, p.approved_at, p.approved_by
                FROM participants p
                WHERE p.workshop_id = %s AND p.user_id = %s
            """, (workshop_id, user_id))
            
            participant = cursor.fetchone()
            
            if participant:
                # Convert datetime to ISO string
                participant['requested_at'] = participant['requested_at'].isoformat() if participant['requested_at'] else None
                participant['approved_at'] = participant['approved_at'].isoformat() if participant['approved_at'] else None
            
            return participant
    
    def update_participant_status(
        self, 
        participant_id: str, 
        status: str,
        approved_by: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Update participant status
        
        Args:
            participant_id: Participant ID
            status: New status (pending, joined, rejected, waitlisted)
            approved_by: User ID of approver (for joined/rejected status)
            
        Returns:
            Updated participant dict or None if not found
        """
        with get_db_cursor() as cursor:
            if approved_by and status in ['joined', 'rejected']:
                cursor.execute("""
                    UPDATE participants
                    SET status = %s, approved_by = %s, approved_at = CURRENT_TIMESTAMP
                    WHERE id = %s
                """, (status, approved_by, participant_id))
            else:
                cursor.execute("""
                    UPDATE participants
                    SET status = %s
                    WHERE id = %s
                """, (status, participant_id))
        
        # Fetch updated participant
        return self.get_participant_by_id(participant_id)
    
    def delete_participant(self, participant_id: str) -> bool:
        """
        Delete participant (leave workshop)
        
        Args:
            participant_id: Participant ID
            
        Returns:
            True if deleted, False if not found
        """
        with get_db_cursor() as cursor:
            cursor.execute("DELETE FROM participants WHERE id = %s", (participant_id,))
            return cursor.rowcount > 0
    
    def get_participant_count(self, workshop_id: str, status: Optional[str] = None) -> int:
        """
        Get count of participants for a workshop
        
        Args:
            workshop_id: Workshop ID
            status: Optional status filter
            
        Returns:
            Count of participants
        """
        with get_db_cursor(commit=False) as cursor:
            if status:
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM participants
                    WHERE workshop_id = %s AND status = %s
                """, (workshop_id, status))
            else:
                cursor.execute("""
                    SELECT COUNT(*) as count
                    FROM participants
                    WHERE workshop_id = %s
                """, (workshop_id,))
            
            result = cursor.fetchone()
            return result['count'] if result else 0
