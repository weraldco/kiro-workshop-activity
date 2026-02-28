"""
Tests for Participant Endpoints - Join Requests and Approval Workflow
"""
import pytest
import json
from app import create_app
from app.store.user_store import UserStore
from app.store.workshop_store_mysql import WorkshopStore
from app.store.participant_store import ParticipantStore
from app.auth import hash_password, generate_access_token
from app.database.connection import get_db_connection, close_db_connection


@pytest.fixture
def app():
    """Create test Flask app"""
    app = create_app({'TESTING': True})
    return app


@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()


@pytest.fixture(autouse=True)
def clean_database():
    """Clean database before each test"""
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM participants")
        cursor.execute("DELETE FROM challenges")
        cursor.execute("DELETE FROM workshops")
        cursor.execute("DELETE FROM users")
        conn.commit()
    finally:
        cursor.close()
        close_db_connection(conn)
    yield


@pytest.fixture
def user_store():
    """Create user store"""
    return UserStore()


@pytest.fixture
def workshop_store():
    """Create workshop store"""
    return WorkshopStore()


@pytest.fixture
def participant_store():
    """Create participant store"""
    return ParticipantStore()


@pytest.fixture
def owner_user(user_store):
    """Create workshop owner user"""
    password_hash = hash_password('OwnerPass123!')
    user = user_store.create_user('owner@example.com', password_hash, 'Workshop Owner')
    return user


@pytest.fixture
def participant_user(user_store):
    """Create participant user"""
    password_hash = hash_password('ParticipantPass123!')
    user = user_store.create_user('participant@example.com', password_hash, 'Participant User')
    return user


@pytest.fixture
def participant_user2(user_store):
    """Create second participant user"""
    password_hash = hash_password('ParticipantPass123!')
    user = user_store.create_user('participant2@example.com', password_hash, 'Participant User 2')
    return user


@pytest.fixture
def owner_token(owner_user):
    """Generate auth token for owner"""
    return generate_access_token(
        user_id=owner_user['id'],
        email=owner_user['email'],
        name=owner_user['name']
    )


@pytest.fixture
def participant_token(participant_user):
    """Generate auth token for participant"""
    return generate_access_token(
        user_id=participant_user['id'],
        email=participant_user['email'],
        name=participant_user['name']
    )


@pytest.fixture
def participant_token2(participant_user2):
    """Generate auth token for second participant"""
    return generate_access_token(
        user_id=participant_user2['id'],
        email=participant_user2['email'],
        name=participant_user2['name']
    )


@pytest.fixture
def test_workshop(workshop_store, owner_user):
    """Create a test workshop"""
    return workshop_store.create_workshop(
        'Test Workshop',
        'Test Description',
        owner_user['id']
    )


class TestJoinWorkshop:
    """Tests for POST /api/workshops/<id>/join"""
    
    def test_join_workshop_success(self, client, test_workshop, participant_token):
        """Test successful workshop join request"""
        response = client.post(f'/api/workshops/{test_workshop["id"]}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 201
        data = json.loads(response.data)
        
        assert 'id' in data
        assert data['workshop_id'] == test_workshop['id']
        assert data['status'] == 'pending'
        assert 'user_name' in data
        assert 'user_email' in data
        assert 'requested_at' in data
    
    def test_join_workshop_without_auth(self, client, test_workshop):
        """Test joining workshop without authentication"""
        response = client.post(f'/api/workshops/{test_workshop["id"]}/join')
        
        assert response.status_code == 401
    
    def test_join_nonexistent_workshop(self, client, participant_token):
        """Test joining non-existent workshop"""
        response = client.post('/api/workshops/nonexistent-id/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 404
    
    def test_owner_cannot_join_own_workshop(self, client, test_workshop, owner_token):
        """Test that workshop owner cannot join their own workshop"""
        response = client.post(f'/api/workshops/{test_workshop["id"]}/join',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'owner' in data['error'].lower()
    
    def test_join_workshop_twice(self, client, test_workshop, participant_token):
        """Test joining same workshop twice"""
        # First join
        client.post(f'/api/workshops/{test_workshop["id"]}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        # Second join
        response = client.post(f'/api/workshops/{test_workshop["id"]}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 409
        data = json.loads(response.data)
        assert 'already' in data['error'].lower()


class TestGetWorkshopParticipants:
    """Tests for GET /api/workshops/<id>/participants"""
    
    def test_get_participants_as_owner(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test getting participants as workshop owner"""
        # Create some participants
        participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        
        response = client.get(f'/api/workshops/{test_workshop["id"]}/participants',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert 'pending' in data
        assert 'joined' in data
        assert 'rejected' in data
        assert 'waitlisted' in data
        assert len(data['pending']) == 1
    
    def test_get_participants_filtered_by_status(self, client, test_workshop, owner_token, participant_store, participant_user, participant_user2):
        """Test getting participants filtered by status"""
        # Create participants with different statuses
        p1 = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        p2 = participant_store.create_participant(test_workshop['id'], participant_user2['id'], 'joined')
        
        response = client.get(f'/api/workshops/{test_workshop["id"]}/participants?status=pending',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]['status'] == 'pending'
    
    def test_get_participants_not_owner(self, client, test_workshop, participant_token):
        """Test getting participants as non-owner"""
        response = client.get(f'/api/workshops/{test_workshop["id"]}/participants',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 403
    
    def test_get_participants_without_auth(self, client, test_workshop):
        """Test getting participants without authentication"""
        response = client.get(f'/api/workshops/{test_workshop["id"]}/participants')
        
        assert response.status_code == 401
    
    def test_get_participants_nonexistent_workshop(self, client, owner_token):
        """Test getting participants for non-existent workshop"""
        response = client.get('/api/workshops/nonexistent-id/participants',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        
        assert response.status_code == 404


class TestUpdateParticipantStatus:
    """Tests for PATCH /api/workshops/<wid>/participants/<pid>"""
    
    def test_approve_participant(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test approving a participant (pending -> joined)"""
        # Create pending participant
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        
        response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({'status': 'joined'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'joined'
        assert data['approved_at'] is not None
        assert data['approved_by'] is not None
    
    def test_reject_participant(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test rejecting a participant"""
        # Create pending participant
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        
        response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({'status': 'rejected'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'rejected'
        assert data['approved_at'] is not None
        assert data['approved_by'] is not None
    
    def test_waitlist_participant(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test waitlisting a participant"""
        # Create pending participant
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        
        response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({'status': 'waitlisted'}),
            content_type='application/json'
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data['status'] == 'waitlisted'
    
    def test_update_status_not_owner(self, client, test_workshop, participant_token, participant_store, participant_user2):
        """Test updating status as non-owner"""
        # Create participant
        participant = participant_store.create_participant(test_workshop['id'], participant_user2['id'], 'pending')
        
        response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {participant_token}'},
            data=json.dumps({'status': 'joined'}),
            content_type='application/json'
        )
        
        assert response.status_code == 403
    
    def test_update_status_invalid_status(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test updating with invalid status"""
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        
        response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({'status': 'invalid'}),
            content_type='application/json'
        )
        
        assert response.status_code == 400
    
    def test_update_status_missing_status(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test updating without status field"""
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'pending')
        
        response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({}),
            content_type='application/json'
        )
        
        assert response.status_code == 400


class TestRemoveParticipant:
    """Tests for DELETE /api/workshops/<wid>/participants/<pid>"""
    
    def test_owner_removes_participant(self, client, test_workshop, owner_token, participant_store, participant_user):
        """Test owner removing a participant"""
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'joined')
        
        response = client.delete(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        
        assert response.status_code == 204
        
        # Verify participant is deleted
        deleted = participant_store.get_participant_by_id(participant['id'])
        assert deleted is None
    
    def test_participant_leaves_workshop(self, client, test_workshop, participant_token, participant_store, participant_user):
        """Test participant leaving workshop (self-removal)"""
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'joined')
        
        response = client.delete(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 204
    
    def test_remove_participant_unauthorized(self, client, test_workshop, participant_token2, participant_store, participant_user):
        """Test removing participant by unauthorized user"""
        participant = participant_store.create_participant(test_workshop['id'], participant_user['id'], 'joined')
        
        response = client.delete(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {participant_token2}'}
        )
        
        assert response.status_code == 403


class TestGetJoinedWorkshops:
    """Tests for GET /api/workshops/joined"""
    
    def test_get_joined_workshops(self, client, workshop_store, owner_user, participant_user, participant_token, participant_store):
        """Test getting workshops user has joined"""
        # Create workshops
        workshop1 = workshop_store.create_workshop('Workshop 1', 'Description 1', owner_user['id'])
        workshop2 = workshop_store.create_workshop('Workshop 2', 'Description 2', owner_user['id'])
        
        # Join workshops
        participant_store.create_participant(workshop1['id'], participant_user['id'], 'joined')
        participant_store.create_participant(workshop2['id'], participant_user['id'], 'pending')
        
        response = client.get('/api/workshops/joined',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert len(data) == 2
        assert 'workshop_title' in data[0]
        assert 'workshop_description' in data[0]
        assert 'status' in data[0]
    
    def test_get_joined_workshops_empty(self, client, participant_token):
        """Test getting joined workshops when user hasn't joined any"""
        response = client.get('/api/workshops/joined',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        assert data == []
    
    def test_get_joined_workshops_without_auth(self, client):
        """Test getting joined workshops without authentication"""
        response = client.get('/api/workshops/joined')
        
        assert response.status_code == 401


class TestParticipantWorkflow:
    """Integration tests for complete participant workflow"""
    
    def test_full_approval_workflow(self, client, test_workshop, owner_token, participant_token, participant_store):
        """Test complete workflow: join → approve → verify"""
        # 1. Participant joins workshop
        join_response = client.post(f'/api/workshops/{test_workshop["id"]}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert join_response.status_code == 201
        participant = json.loads(join_response.data)
        assert participant['status'] == 'pending'
        
        # 2. Owner views pending requests
        pending_response = client.get(
            f'/api/workshops/{test_workshop["id"]}/participants?status=pending',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        
        assert pending_response.status_code == 200
        pending = json.loads(pending_response.data)
        assert len(pending) == 1
        
        # 3. Owner approves request
        approve_response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({'status': 'joined'}),
            content_type='application/json'
        )
        
        assert approve_response.status_code == 200
        approved = json.loads(approve_response.data)
        assert approved['status'] == 'joined'
        
        # 4. Participant views joined workshops
        joined_response = client.get('/api/workshops/joined',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        assert joined_response.status_code == 200
        joined = json.loads(joined_response.data)
        assert len(joined) == 1
        assert joined[0]['status'] == 'joined'
    
    def test_rejection_workflow(self, client, test_workshop, owner_token, participant_token):
        """Test workflow: join → reject"""
        # Join workshop
        join_response = client.post(f'/api/workshops/{test_workshop["id"]}/join',
            headers={'Authorization': f'Bearer {participant_token}'}
        )
        
        participant = json.loads(join_response.data)
        
        # Reject request
        reject_response = client.patch(
            f'/api/workshops/{test_workshop["id"]}/participants/{participant["id"]}',
            headers={'Authorization': f'Bearer {owner_token}'},
            data=json.dumps({'status': 'rejected'}),
            content_type='application/json'
        )
        
        assert reject_response.status_code == 200
        rejected = json.loads(reject_response.data)
        assert rejected['status'] == 'rejected'
