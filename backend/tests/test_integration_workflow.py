"""
Integration Tests - Full User Workflows
Tests complete user journeys through the system
"""
import pytest
from app import create_app
from app.database.connection import get_db_connection
from app.store.user_store import UserStore
from app.store.workshop_store_mysql import WorkshopStore
from app.store.participant_store import ParticipantStore


@pytest.fixture
def app():
    """Create test app"""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test"""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM participants")
        cursor.execute("DELETE FROM workshops")
        cursor.execute("DELETE FROM users")
        conn.commit()
    finally:
        cursor.close()
        conn.close()
    yield


class TestCompleteWorkflow:
    """Test complete user workflows"""
    
    def test_full_workshop_creation_and_join_workflow(self, client):
        """
        Test complete workflow:
        1. User A registers
        2. User A creates workshop
        3. User B registers
        4. User B joins workshop
        5. User A approves join request
        6. User B is now a participant
        """
        # Step 1: User A registers
        response = client.post('/api/auth/register', json={
            'email': 'owner@example.com',
            'password': 'Owner123!@#',
            'name': 'Workshop Owner'
        })
        assert response.status_code == 201
        owner_data = response.get_json()
        owner_token = owner_data['access_token']
        owner_id = owner_data['id']
        
        # Step 2: User A creates workshop
        response = client.post('/api/workshops', 
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Python Workshop',
                'description': 'Learn Python basics'
            }
        )
        assert response.status_code == 201
        workshop_data = response.get_json()
        workshop_id = workshop_data['id']
        assert workshop_data['owner_id'] == owner_id
        assert workshop_data['signup_enabled'] is True
        
        # Step 3: User B registers
        response = client.post('/api/auth/register', json={
            'email': 'participant@example.com',
            'password': 'Participant123!@#',
            'name': 'Workshop Participant'
        })
        assert response.status_code == 201
        participant_data = response.get_json()
        participant_token = participant_data['access_token']
        participant_user_id = participant_data['id']
        
        # Step 4: User B joins workshop
        response = client.post(f'/api/workshops/{workshop_id}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        assert response.status_code == 201
        join_data = response.get_json()
        participation_id = join_data['id']
        assert join_data['status'] == 'pending'
        assert join_data['user_id'] == participant_user_id
        
        # Step 5: User A views pending requests
        response = client.get(f'/api/workshops/{workshop_id}/participants',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        assert response.status_code == 200
        participants_data = response.get_json()
        assert len(participants_data['pending']) == 1
        assert len(participants_data['joined']) == 0
        assert participants_data['pending'][0]['id'] == participation_id
        
        # Step 6: User A approves join request
        response = client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_id}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'joined'}
        )
        assert response.status_code == 200
        updated_data = response.get_json()
        assert updated_data['status'] == 'joined'
        assert updated_data['approved_by'] == owner_id
        assert updated_data['approved_at'] is not None
        
        # Step 7: Verify User B sees workshop in joined list
        response = client.get('/api/workshops/joined',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        assert response.status_code == 200
        joined_workshops = response.get_json()
        assert len(joined_workshops) == 1
        assert joined_workshops[0]['workshop_id'] == workshop_id
        assert joined_workshops[0]['status'] == 'joined'
    
    def test_workshop_rejection_workflow(self, client):
        """
        Test rejection workflow:
        1. Owner creates workshop
        2. User joins
        3. Owner rejects request
        """
        # Create owner and workshop
        response = client.post('/api/auth/register', json={
            'email': 'owner@example.com',
            'password': 'Owner123!@#',
            'name': 'Workshop Owner'
        })
        owner_token = response.get_json()['access_token']
        
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Exclusive Workshop',
                'description': 'Limited seats'
            }
        )
        workshop_id = response.get_json()['id']
        
        # Create participant and join
        response = client.post('/api/auth/register', json={
            'email': 'participant@example.com',
            'password': 'Participant123!@#',
            'name': 'Workshop Participant'
        })
        participant_token = response.get_json()['access_token']
        
        response = client.post(f'/api/workshops/{workshop_id}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        participation_id = response.get_json()['id']
        
        # Owner rejects request
        response = client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_id}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'rejected'}
        )
        assert response.status_code == 200
        assert response.get_json()['status'] == 'rejected'
        
        # Verify participant sees rejected status
        response = client.get('/api/workshops/joined',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        joined_workshops = response.get_json()
        assert len(joined_workshops) == 1
        assert joined_workshops[0]['status'] == 'rejected'
    
    def test_participant_leave_workflow(self, client):
        """
        Test leave workflow:
        1. User joins and gets approved
        2. User leaves workshop
        """
        # Create owner and workshop
        response = client.post('/api/auth/register', json={
            'email': 'owner@example.com',
            'password': 'Owner123!@#',
            'name': 'Workshop Owner'
        })
        owner_token = response.get_json()['access_token']
        
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Test Workshop',
                'description': 'Test description'
            }
        )
        workshop_id = response.get_json()['id']
        
        # Create participant, join, and get approved
        response = client.post('/api/auth/register', json={
            'email': 'participant@example.com',
            'password': 'Participant123!@#',
            'name': 'Workshop Participant'
        })
        participant_token = response.get_json()['access_token']
        
        response = client.post(f'/api/workshops/{workshop_id}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        participation_id = response.get_json()['id']
        
        # Approve
        client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_id}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'joined'}
        )
        
        # Participant leaves
        response = client.delete(
            f'/api/workshops/{workshop_id}/participants/{participation_id}',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        assert response.status_code == 204
        
        # Verify participant no longer in list
        response = client.get('/api/workshops/joined',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        joined_workshops = response.get_json()
        assert len(joined_workshops) == 0
    
    def test_owner_remove_participant_workflow(self, client):
        """
        Test owner removing participant:
        1. User joins and gets approved
        2. Owner removes participant
        """
        # Create owner and workshop
        response = client.post('/api/auth/register', json={
            'email': 'owner@example.com',
            'password': 'Owner123!@#',
            'name': 'Workshop Owner'
        })
        owner_token = response.get_json()['access_token']
        
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Test Workshop',
                'description': 'Test description'
            }
        )
        workshop_id = response.get_json()['id']
        
        # Create participant, join, and get approved
        response = client.post('/api/auth/register', json={
            'email': 'participant@example.com',
            'password': 'Participant123!@#',
            'name': 'Workshop Participant'
        })
        participant_token = response.get_json()['access_token']
        
        response = client.post(f'/api/workshops/{workshop_id}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        participation_id = response.get_json()['id']
        
        # Approve
        client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_id}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'joined'}
        )
        
        # Owner removes participant
        response = client.delete(
            f'/api/workshops/{workshop_id}/participants/{participation_id}',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        assert response.status_code == 204
        
        # Verify participant removed
        response = client.get(f'/api/workshops/{workshop_id}/participants',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        participants_data = response.get_json()
        assert len(participants_data['joined']) == 0
    
    def test_multiple_participants_workflow(self, client):
        """
        Test multiple participants joining same workshop
        """
        # Create owner and workshop
        response = client.post('/api/auth/register', json={
            'email': 'owner@example.com',
            'password': 'Owner123!@#',
            'name': 'Workshop Owner'
        })
        owner_token = response.get_json()['access_token']
        
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Popular Workshop',
                'description': 'Many participants'
            }
        )
        workshop_id = response.get_json()['id']
        
        # Create 3 participants
        participant_tokens = []
        participation_ids = []
        
        for i in range(3):
            response = client.post('/api/auth/register', json={
                'email': f'participant{i}@example.com',
                'password': 'Participant123!@#',
                'name': f'Participant {i}'
            })
            token = response.get_json()['access_token']
            participant_tokens.append(token)
            
            # Join workshop
            response = client.post(f'/api/workshops/{workshop_id}/join',
                headers={'Authorization': f'Bearer {token}'}
            )
            participation_ids.append(response.get_json()['id'])
        
        # Verify 3 pending requests
        response = client.get(f'/api/workshops/{workshop_id}/participants',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        participants_data = response.get_json()
        assert len(participants_data['pending']) == 3
        
        # Approve first two, reject third
        client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_ids[0]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'joined'}
        )
        client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_ids[1]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'joined'}
        )
        client.patch(
            f'/api/workshops/{workshop_id}/participants/{participation_ids[2]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={'status': 'rejected'}
        )
        
        # Verify final state
        response = client.get(f'/api/workshops/{workshop_id}/participants',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        participants_data = response.get_json()
        assert len(participants_data['joined']) == 2
        assert len(participants_data['rejected']) == 1
        assert len(participants_data['pending']) == 0
    
    def test_workshop_update_workflow(self, client):
        """
        Test workshop update workflow
        """
        # Create owner and workshop
        response = client.post('/api/auth/register', json={
            'email': 'owner@example.com',
            'password': 'Owner123!@#',
            'name': 'Workshop Owner'
        })
        owner_token = response.get_json()['access_token']
        
        response = client.post('/api/workshops',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Initial Title',
                'description': 'Initial description'
            }
        )
        workshop_id = response.get_json()['id']
        
        # Update workshop
        response = client.patch(f'/api/workshops/{workshop_id}',
            headers={'Authorization': f'Bearer {owner_token}'},
            json={
                'title': 'Updated Title',
                'description': 'Updated description',
                'status': 'ongoing',
                'signup_enabled': False
            }
        )
        assert response.status_code == 200
        updated_data = response.get_json()
        assert updated_data['title'] == 'Updated Title'
        assert updated_data['description'] == 'Updated description'
        assert updated_data['status'] == 'ongoing'
        assert updated_data['signup_enabled'] is False
        
        # Verify updates persisted
        response = client.get(f'/api/workshops/{workshop_id}')
        workshop_data = response.get_json()
        assert workshop_data['title'] == 'Updated Title'
        assert workshop_data['signup_enabled'] is False
