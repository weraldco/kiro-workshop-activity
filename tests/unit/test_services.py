"""
Unit tests for business logic services.

Tests the workshop, challenge, and registration services to ensure they
correctly interact with the data store and implement business logic.
"""

import os
import tempfile
import pytest
from datetime import datetime

from app.store.workshop_store import WorkshopStore
from app.services.workshop_service import WorkshopService
from app.services.challenge_service import ChallengeService
from app.services.registration_service import RegistrationService


@pytest.fixture
def temp_store():
    """Create a temporary store for testing."""
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    # Remove the empty file so WorkshopStore can initialize it properly
    os.remove(path)
    store = WorkshopStore(path)
    yield store
    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@pytest.fixture
def workshop_service(temp_store):
    """Create a workshop service with temporary store."""
    return WorkshopService(temp_store)


@pytest.fixture
def challenge_service(temp_store):
    """Create a challenge service with temporary store."""
    return ChallengeService(temp_store)


@pytest.fixture
def registration_service(temp_store):
    """Create a registration service with temporary store."""
    return RegistrationService(temp_store)


class TestWorkshopService:
    """Tests for WorkshopService."""
    
    def test_create_workshop_generates_id(self, workshop_service):
        """Test that create_workshop generates a unique ID."""
        data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        
        workshop = workshop_service.create_workshop(data)
        
        assert 'id' in workshop
        assert workshop['id'] is not None
        assert len(workshop['id']) > 0
    
    def test_create_workshop_initializes_registration_count(self, workshop_service):
        """Test that create_workshop initializes registration_count to 0."""
        data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        
        workshop = workshop_service.create_workshop(data)
        
        assert workshop['registration_count'] == 0
    
    def test_get_workshop_returns_created_workshop(self, workshop_service):
        """Test that get_workshop retrieves a created workshop."""
        data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        
        created = workshop_service.create_workshop(data)
        retrieved = workshop_service.get_workshop(created['id'])
        
        assert retrieved is not None
        assert retrieved['id'] == created['id']
        assert retrieved['title'] == data['title']
    
    def test_get_workshop_returns_none_for_nonexistent(self, workshop_service):
        """Test that get_workshop returns None for non-existent ID."""
        result = workshop_service.get_workshop('nonexistent-id')
        assert result is None
    
    def test_list_workshops_returns_all_workshops(self, workshop_service):
        """Test that list_workshops returns all created workshops."""
        data1 = {
            'title': 'Workshop 1',
            'description': 'First workshop',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        data2 = {
            'title': 'Workshop 2',
            'description': 'Second workshop',
            'start_time': '2024-06-02T10:00:00',
            'end_time': '2024-06-02T12:00:00',
            'capacity': 15,
            'delivery_mode': 'face-to-face'
        }
        
        workshop_service.create_workshop(data1)
        workshop_service.create_workshop(data2)
        
        workshops = workshop_service.list_workshops()
        
        assert len(workshops) == 2
        assert workshops[0]['title'] == 'Workshop 1'
        assert workshops[1]['title'] == 'Workshop 2'
    
    def test_workshop_exists_returns_true_for_existing(self, workshop_service):
        """Test that workshop_exists returns True for existing workshop."""
        data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        
        workshop = workshop_service.create_workshop(data)
        
        assert workshop_service.workshop_exists(workshop['id']) is True
    
    def test_workshop_exists_returns_false_for_nonexistent(self, workshop_service):
        """Test that workshop_exists returns False for non-existent workshop."""
        assert workshop_service.workshop_exists('nonexistent-id') is False


class TestChallengeService:
    """Tests for ChallengeService."""
    
    def test_create_challenge_generates_id(self, workshop_service, challenge_service):
        """Test that create_challenge generates a unique ID."""
        # Create a workshop first
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Create a challenge
        challenge_data = {
            'title': 'Build a Calculator',
            'description': 'Create a simple calculator app'
        }
        challenge = challenge_service.create_challenge(workshop['id'], challenge_data)
        
        assert 'id' in challenge
        assert challenge['id'] is not None
        assert len(challenge['id']) > 0
    
    def test_create_challenge_includes_timestamp(self, workshop_service, challenge_service):
        """Test that create_challenge includes created_at timestamp."""
        # Create a workshop first
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Create a challenge
        challenge_data = {
            'title': 'Build a Calculator',
            'description': 'Create a simple calculator app'
        }
        challenge = challenge_service.create_challenge(workshop['id'], challenge_data)
        
        assert 'created_at' in challenge
        assert challenge['created_at'] is not None
        # Verify it's a valid ISO 8601 timestamp
        datetime.fromisoformat(challenge['created_at'])
    
    def test_list_challenges_returns_workshop_challenges(self, workshop_service, challenge_service):
        """Test that list_challenges returns challenges for specific workshop."""
        # Create two workshops
        workshop1_data = {
            'title': 'Workshop 1',
            'description': 'First workshop',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop2_data = {
            'title': 'Workshop 2',
            'description': 'Second workshop',
            'start_time': '2024-06-02T10:00:00',
            'end_time': '2024-06-02T12:00:00',
            'capacity': 15,
            'delivery_mode': 'face-to-face'
        }
        workshop1 = workshop_service.create_workshop(workshop1_data)
        workshop2 = workshop_service.create_workshop(workshop2_data)
        
        # Create challenges for both workshops
        challenge_service.create_challenge(workshop1['id'], {'title': 'Challenge 1A'})
        challenge_service.create_challenge(workshop1['id'], {'title': 'Challenge 1B'})
        challenge_service.create_challenge(workshop2['id'], {'title': 'Challenge 2A'})
        
        # List challenges for workshop 1
        challenges = challenge_service.list_challenges(workshop1['id'])
        
        assert len(challenges) == 2
        assert all(c['workshop_id'] == workshop1['id'] for c in challenges)


class TestRegistrationService:
    """Tests for RegistrationService."""
    
    def test_register_participant_generates_id(self, workshop_service, registration_service):
        """Test that register_participant generates a unique ID."""
        # Create a workshop first
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Register a participant
        registration_data = {
            'participant_name': 'John Doe',
            'participant_email': 'john@example.com'
        }
        registration, error = registration_service.register_participant(workshop['id'], registration_data)
        
        assert error == ""
        assert registration is not None
        assert 'id' in registration
        assert registration['id'] is not None
        assert len(registration['id']) > 0
    
    def test_register_participant_increments_count(self, workshop_service, registration_service):
        """Test that register_participant increments workshop registration count."""
        # Create a workshop
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Register a participant
        registration_data = {
            'participant_name': 'John Doe',
            'participant_email': 'john@example.com'
        }
        registration_service.register_participant(workshop['id'], registration_data)
        
        # Check that count was incremented
        updated_workshop = workshop_service.get_workshop(workshop['id'])
        assert updated_workshop['registration_count'] == 1
    
    def test_register_participant_enforces_capacity(self, workshop_service, registration_service):
        """Test that register_participant enforces capacity limit."""
        # Create a workshop with capacity of 1
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 1,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Register first participant (should succeed)
        registration_data1 = {
            'participant_name': 'John Doe',
            'participant_email': 'john@example.com'
        }
        registration1, error1 = registration_service.register_participant(workshop['id'], registration_data1)
        assert error1 == ""
        assert registration1 is not None
        
        # Try to register second participant (should fail)
        registration_data2 = {
            'participant_name': 'Jane Smith',
            'participant_email': 'jane@example.com'
        }
        registration2, error2 = registration_service.register_participant(workshop['id'], registration_data2)
        assert registration2 is None
        assert "full" in error2.lower()
    
    def test_list_registrations_returns_all_registrations(self, workshop_service, registration_service):
        """Test that list_registrations returns all registrations."""
        # Create a workshop
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Register two participants
        registration_service.register_participant(workshop['id'], {
            'participant_name': 'John Doe',
            'participant_email': 'john@example.com'
        })
        registration_service.register_participant(workshop['id'], {
            'participant_name': 'Jane Smith',
            'participant_email': 'jane@example.com'
        })
        
        # List all registrations
        registrations = registration_service.list_registrations()
        
        assert len(registrations) == 2
    
    def test_get_registration_count_returns_correct_count(self, workshop_service, registration_service):
        """Test that get_registration_count returns correct count."""
        # Create a workshop
        workshop_data = {
            'title': 'Python Workshop',
            'description': 'Learn Python basics',
            'start_time': '2024-06-01T10:00:00',
            'end_time': '2024-06-01T12:00:00',
            'capacity': 20,
            'delivery_mode': 'online'
        }
        workshop = workshop_service.create_workshop(workshop_data)
        
        # Initially should be 0
        assert registration_service.get_registration_count(workshop['id']) == 0
        
        # Register a participant
        registration_service.register_participant(workshop['id'], {
            'participant_name': 'John Doe',
            'participant_email': 'john@example.com'
        })
        
        # Should now be 1
        assert registration_service.get_registration_count(workshop['id']) == 1
