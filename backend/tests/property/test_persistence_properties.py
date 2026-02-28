"""
Property-based tests for data persistence.

Tests verify that data persists correctly across save/load cycles.
"""

import os
import tempfile
import uuid
from datetime import datetime, timedelta

import pytest
from hypothesis import given, settings
import hypothesis.strategies as st

from app.store.workshop_store import WorkshopStore


# Custom strategies for generating valid test data
@st.composite
def valid_workshop(draw):
    """Generate a valid workshop with all required fields."""
    start_time = draw(st.datetimes(
        min_value=datetime(2024, 1, 1),
        max_value=datetime(2025, 12, 31)
    ))
    end_time = start_time + timedelta(hours=draw(st.integers(min_value=1, max_value=48)))
    
    return {
        'id': str(uuid.uuid4()),
        'title': draw(st.text(min_size=1, max_size=100).filter(lambda s: s.strip())),
        'description': draw(st.text(max_size=500)),
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': draw(st.integers(min_value=1, max_value=1000)),
        'delivery_mode': draw(st.sampled_from(['online', 'face-to-face', 'hybrid'])),
        'registration_count': draw(st.integers(min_value=0, max_value=100))
    }


@st.composite
def valid_challenge(draw, workshop_id=None):
    """Generate a valid challenge with all required fields."""
    if workshop_id is None:
        workshop_id = str(uuid.uuid4())
    
    return {
        'id': str(uuid.uuid4()),
        'workshop_id': workshop_id,
        'title': draw(st.text(min_size=1, max_size=100).filter(lambda s: s.strip())),
        'description': draw(st.text(max_size=500)),
        'created_at': draw(st.datetimes(
            min_value=datetime(2024, 1, 1),
            max_value=datetime(2025, 12, 31)
        )).isoformat()
    }


@st.composite
def valid_registration(draw, workshop_id=None):
    """Generate a valid registration with all required fields."""
    if workshop_id is None:
        workshop_id = str(uuid.uuid4())
    
    return {
        'id': str(uuid.uuid4()),
        'workshop_id': workshop_id,
        'participant_name': draw(st.text(min_size=1, max_size=100).filter(lambda s: s.strip())),
        'participant_email': draw(st.emails()),
        'registered_at': draw(st.datetimes(
            min_value=datetime(2024, 1, 1),
            max_value=datetime(2025, 12, 31)
        )).isoformat()
    }


@pytest.fixture
def temp_store():
    """Create a temporary store for testing."""
    # Create a temporary file
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    
    # Create store
    store = WorkshopStore(path)
    
    yield store
    
    # Cleanup
    if os.path.exists(path):
        os.remove(path)


@settings(max_examples=100)
@given(workshop=valid_workshop())
def test_property_6_workshop_persistence_round_trip(workshop):
    """
    **Validates: Requirements 1.8, 9.1, 9.4**
    
    Feature: workshop-management, Property 6: Persistence Round-Trip
    For any workshop created through the API, reloading the data from the JSON file
    should return an equivalent entity with all fields preserved.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    # Remove the file so WorkshopStore can initialize it properly
    os.remove(path)
    
    try:
        # Create store and add workshop
        store = WorkshopStore(path)
        store.add_workshop(workshop)
        
        # Create a new store instance to force reload from file
        store2 = WorkshopStore(path)
        loaded_workshop = store2.get_workshop(workshop['id'])
        
        # Verify all fields are preserved
        assert loaded_workshop is not None, "Workshop should be retrievable after persistence"
        assert loaded_workshop['id'] == workshop['id']
        assert loaded_workshop['title'] == workshop['title']
        assert loaded_workshop['description'] == workshop['description']
        assert loaded_workshop['start_time'] == workshop['start_time']
        assert loaded_workshop['end_time'] == workshop['end_time']
        assert loaded_workshop['capacity'] == workshop['capacity']
        assert loaded_workshop['delivery_mode'] == workshop['delivery_mode']
        assert loaded_workshop['registration_count'] == workshop['registration_count']
        
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(challenge=valid_challenge())
def test_property_6_challenge_persistence_round_trip(challenge):
    """
    **Validates: Requirements 4.6, 9.2, 9.4**
    
    Feature: workshop-management, Property 6: Persistence Round-Trip
    For any challenge created through the API, reloading the data from the JSON file
    should return an equivalent entity with all fields preserved.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    # Remove the file so WorkshopStore can initialize it properly
    os.remove(path)
    
    try:
        # Create store and add challenge
        store = WorkshopStore(path)
        store.add_challenge(challenge)
        
        # Create a new store instance to force reload from file
        store2 = WorkshopStore(path)
        loaded_challenges = store2.get_challenges(challenge['workshop_id'])
        
        # Verify challenge is in the loaded data
        assert len(loaded_challenges) == 1, "Challenge should be retrievable after persistence"
        loaded_challenge = loaded_challenges[0]
        
        # Verify all fields are preserved
        assert loaded_challenge['id'] == challenge['id']
        assert loaded_challenge['workshop_id'] == challenge['workshop_id']
        assert loaded_challenge['title'] == challenge['title']
        assert loaded_challenge['description'] == challenge['description']
        assert loaded_challenge['created_at'] == challenge['created_at']
        
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(registration=valid_registration())
def test_property_6_registration_persistence_round_trip(registration):
    """
    **Validates: Requirements 6.6, 9.3, 9.4**
    
    Feature: workshop-management, Property 6: Persistence Round-Trip
    For any registration created through the API, reloading the data from the JSON file
    should return an equivalent entity with all fields preserved.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    # Remove the file so WorkshopStore can initialize it properly
    os.remove(path)
    
    try:
        # Create store and add registration
        store = WorkshopStore(path)
        store.add_registration(registration)
        
        # Create a new store instance to force reload from file
        store2 = WorkshopStore(path)
        loaded_registrations = store2.get_registrations_for_workshop(registration['workshop_id'])
        
        # Verify registration is in the loaded data
        assert len(loaded_registrations) == 1, "Registration should be retrievable after persistence"
        loaded_registration = loaded_registrations[0]
        
        # Verify all fields are preserved
        assert loaded_registration['id'] == registration['id']
        assert loaded_registration['workshop_id'] == registration['workshop_id']
        assert loaded_registration['participant_name'] == registration['participant_name']
        assert loaded_registration['participant_email'] == registration['participant_email']
        assert loaded_registration['registered_at'] == registration['registered_at']
        
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(
    workshops=st.lists(valid_workshop(), min_size=1, max_size=10),
    challenges=st.lists(valid_challenge(), min_size=1, max_size=10),
    registrations=st.lists(valid_registration(), min_size=1, max_size=10)
)
def test_property_6_multiple_entities_persistence_round_trip(workshops, challenges, registrations):
    """
    **Validates: Requirements 1.8, 4.6, 6.6, 9.1, 9.2, 9.3, 9.4**
    
    Feature: workshop-management, Property 6: Persistence Round-Trip
    For any combination of workshops, challenges, and registrations created through the API,
    reloading the data from the JSON file should return all entities with all fields preserved.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    # Remove the file so WorkshopStore can initialize it properly
    os.remove(path)
    
    try:
        # Create store and add all entities
        store = WorkshopStore(path)
        
        for workshop in workshops:
            store.add_workshop(workshop)
        
        for challenge in challenges:
            store.add_challenge(challenge)
        
        for registration in registrations:
            store.add_registration(registration)
        
        # Create a new store instance to force reload from file
        store2 = WorkshopStore(path)
        
        # Verify all workshops are preserved
        loaded_workshops = store2.get_all_workshops()
        assert len(loaded_workshops) == len(workshops), "All workshops should be retrievable"
        
        for workshop in workshops:
            loaded_workshop = store2.get_workshop(workshop['id'])
            assert loaded_workshop is not None
            assert loaded_workshop == workshop
        
        # Verify all challenges are preserved
        loaded_all_challenges = store2.load_data()['challenges']
        assert len(loaded_all_challenges) == len(challenges), "All challenges should be retrievable"
        
        for challenge in challenges:
            loaded_challenges = store2.get_challenges(challenge['workshop_id'])
            matching = [c for c in loaded_challenges if c['id'] == challenge['id']]
            assert len(matching) == 1
            assert matching[0] == challenge
        
        # Verify all registrations are preserved
        loaded_all_registrations = store2.get_all_registrations()
        assert len(loaded_all_registrations) == len(registrations), "All registrations should be retrievable"
        
        for registration in registrations:
            loaded_registrations = store2.get_registrations_for_workshop(registration['workshop_id'])
            matching = [r for r in loaded_registrations if r['id'] == registration['id']]
            assert len(matching) == 1
            assert matching[0] == registration
        
    finally:
        # Cleanup
        if os.path.exists(path):
            os.remove(path)


# New property tests for workshop status management feature

@st.composite
def valid_workshop_without_new_fields(draw):
    """Generate a valid workshop WITHOUT status and signup_enabled fields (old format)."""
    start_time = draw(st.datetimes(
        min_value=datetime(2024, 1, 1),
        max_value=datetime(2025, 12, 31)
    ))
    end_time = start_time + timedelta(hours=draw(st.integers(min_value=1, max_value=48)))
    
    return {
        'id': str(uuid.uuid4()),
        'title': draw(st.text(min_size=1, max_size=100).filter(lambda s: s.strip())),
        'description': draw(st.text(max_size=500)),
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': draw(st.integers(min_value=1, max_value=1000)),
        'delivery_mode': draw(st.sampled_from(['online', 'face-to-face', 'hybrid'])),
        'registration_count': draw(st.integers(min_value=0, max_value=100))
    }


@st.composite
def valid_workshop_with_new_fields(draw):
    """Generate a valid workshop WITH status and signup_enabled fields."""
    start_time = draw(st.datetimes(
        min_value=datetime(2024, 1, 1),
        max_value=datetime(2025, 12, 31)
    ))
    end_time = start_time + timedelta(hours=draw(st.integers(min_value=1, max_value=48)))
    
    return {
        'id': str(uuid.uuid4()),
        'title': draw(st.text(min_size=1, max_size=100).filter(lambda s: s.strip())),
        'description': draw(st.text(max_size=500)),
        'start_time': start_time.isoformat(),
        'end_time': end_time.isoformat(),
        'capacity': draw(st.integers(min_value=1, max_value=1000)),
        'delivery_mode': draw(st.sampled_from(['online', 'face-to-face', 'hybrid'])),
        'registration_count': draw(st.integers(min_value=0, max_value=100)),
        'status': draw(st.sampled_from(['pending', 'ongoing', 'completed'])),
        'signup_enabled': draw(st.booleans())
    }


@st.composite
def valid_challenge_with_html(draw, workshop_id=None):
    """Generate a valid challenge with html_content field."""
    if workshop_id is None:
        workshop_id = str(uuid.uuid4())
    
    return {
        'id': str(uuid.uuid4()),
        'workshop_id': workshop_id,
        'title': draw(st.text(min_size=1, max_size=100).filter(lambda s: s.strip())),
        'description': draw(st.text(max_size=500)),
        'html_content': draw(st.text(max_size=5000)),  # Including empty strings
        'created_at': draw(st.datetimes(
            min_value=datetime(2024, 1, 1),
            max_value=datetime(2025, 12, 31)
        )).isoformat()
    }


@settings(max_examples=100)
@given(workshop=valid_workshop_without_new_fields())
def test_property_1_default_field_initialization(workshop):
    """
    **Validates: Requirements 1.1, 4.1**
    
    Feature: workshop-status-management-and-frontend, Property 1: Default Field Initialization
    For any workshop created through the API, the workshop should have status initialized 
    to "pending" and signup_enabled initialized to true.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    os.remove(path)
    
    try:
        # Create store and add workshop without new fields
        store = WorkshopStore(path)
        store.add_workshop(workshop)
        
        # Retrieve the workshop
        loaded_workshop = store.get_workshop(workshop['id'])
        
        # Verify default values are applied
        assert loaded_workshop is not None, "Workshop should be retrievable"
        assert loaded_workshop['status'] == 'pending', "Status should default to 'pending'"
        assert loaded_workshop['signup_enabled'] is True, "signup_enabled should default to True"
        
    finally:
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(workshop=valid_workshop_with_new_fields())
def test_property_3_new_fields_persistence_round_trip(workshop):
    """
    **Validates: Requirements 1.3, 2.5, 4.5, 7.3, 8.4**
    
    Feature: workshop-status-management-and-frontend, Property 3: New Fields Persistence Round-Trip
    For any workshop with status and signup_enabled fields, or challenge with html_content field,
    saving to the JSON file and reloading should preserve all field values exactly.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    os.remove(path)
    
    try:
        # Create store and add workshop with new fields
        store = WorkshopStore(path)
        store.add_workshop(workshop)
        
        # Create a new store instance to force reload from file
        store2 = WorkshopStore(path)
        loaded_workshop = store2.get_workshop(workshop['id'])
        
        # Verify all fields including new ones are preserved
        assert loaded_workshop is not None, "Workshop should be retrievable after persistence"
        assert loaded_workshop['id'] == workshop['id']
        assert loaded_workshop['title'] == workshop['title']
        assert loaded_workshop['description'] == workshop['description']
        assert loaded_workshop['start_time'] == workshop['start_time']
        assert loaded_workshop['end_time'] == workshop['end_time']
        assert loaded_workshop['capacity'] == workshop['capacity']
        assert loaded_workshop['delivery_mode'] == workshop['delivery_mode']
        assert loaded_workshop['registration_count'] == workshop['registration_count']
        assert loaded_workshop['status'] == workshop['status'], "Status should be preserved"
        assert loaded_workshop['signup_enabled'] == workshop['signup_enabled'], "signup_enabled should be preserved"
        
    finally:
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(challenge=valid_challenge_with_html())
def test_property_3_challenge_html_content_persistence(challenge):
    """
    **Validates: Requirements 1.3, 2.5, 4.5, 7.3, 8.4**
    
    Feature: workshop-status-management-and-frontend, Property 3: New Fields Persistence Round-Trip
    For any challenge with html_content field, saving to the JSON file and reloading 
    should preserve the html_content value exactly.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    os.remove(path)
    
    try:
        # Create store and add challenge with html_content
        store = WorkshopStore(path)
        store.add_challenge(challenge)
        
        # Create a new store instance to force reload from file
        store2 = WorkshopStore(path)
        loaded_challenges = store2.get_challenges(challenge['workshop_id'])
        
        # Verify challenge is in the loaded data
        assert len(loaded_challenges) == 1, "Challenge should be retrievable after persistence"
        loaded_challenge = loaded_challenges[0]
        
        # Verify all fields including html_content are preserved
        assert loaded_challenge['id'] == challenge['id']
        assert loaded_challenge['workshop_id'] == challenge['workshop_id']
        assert loaded_challenge['title'] == challenge['title']
        assert loaded_challenge['description'] == challenge['description']
        assert loaded_challenge['html_content'] == challenge['html_content'], "html_content should be preserved"
        assert loaded_challenge['created_at'] == challenge['created_at']
        
    finally:
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(workshop=valid_workshop_without_new_fields())
def test_property_25_default_values_for_missing_fields(workshop):
    """
    **Validates: Requirements 15.1, 15.2, 15.3**
    
    Feature: workshop-status-management-and-frontend, Property 25: Default Values for Missing Fields
    For any workshop loaded from storage that lacks status or signup_enabled fields,
    the workshop should have status defaulted to "pending" and signup_enabled defaulted to true.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    os.remove(path)
    
    try:
        # Create store and manually write old format data (bypassing add_workshop to avoid defaults)
        store = WorkshopStore(path)
        data = store.load_data()
        data['workshops'].append(workshop)  # Add workshop without defaults
        store.save_data(data)
        
        # Create a new store instance and load the workshop
        store2 = WorkshopStore(path)
        loaded_workshop = store2.get_workshop(workshop['id'])
        
        # Verify default values are applied on load
        assert loaded_workshop is not None, "Workshop should be retrievable"
        assert loaded_workshop['status'] == 'pending', "Status should default to 'pending' for old data"
        assert loaded_workshop['signup_enabled'] is True, "signup_enabled should default to True for old data"
        
        # Also test get_all_workshops
        all_workshops = store2.get_all_workshops()
        matching = [w for w in all_workshops if w['id'] == workshop['id']]
        assert len(matching) == 1
        assert matching[0]['status'] == 'pending'
        assert matching[0]['signup_enabled'] is True
        
    finally:
        if os.path.exists(path):
            os.remove(path)


@settings(max_examples=100)
@given(workshop=valid_workshop_without_new_fields())
def test_property_26_persistence_of_default_values(workshop):
    """
    **Validates: Requirements 15.4**
    
    Feature: workshop-status-management-and-frontend, Property 26: Persistence of Default Values
    For any workshop that had default values applied for missing fields, when the workshop 
    is updated and saved, the default values should be persisted to the JSON file.
    """
    # Create a temporary file for this test
    fd, path = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    os.remove(path)
    
    try:
        # Create store and manually write old format data
        store = WorkshopStore(path)
        data = store.load_data()
        data['workshops'].append(workshop)  # Add workshop without defaults
        store.save_data(data)
        
        # Load the workshop (which applies defaults)
        loaded_workshop = store.get_workshop(workshop['id'])
        assert loaded_workshop is not None
        
        # Update the workshop (this should persist the defaults)
        loaded_workshop['title'] = loaded_workshop['title'] + ' Updated'
        store.update_workshop(loaded_workshop)
        
        # Create a new store instance and load raw data
        store2 = WorkshopStore(path)
        raw_data = store2.load_data()
        
        # Find the workshop in raw data
        raw_workshop = None
        for w in raw_data['workshops']:
            if w['id'] == workshop['id']:
                raw_workshop = w
                break
        
        # Verify defaults are now persisted in the JSON file
        assert raw_workshop is not None, "Workshop should exist in raw data"
        assert 'status' in raw_workshop, "Status should be persisted in JSON"
        assert 'signup_enabled' in raw_workshop, "signup_enabled should be persisted in JSON"
        assert raw_workshop['status'] == 'pending', "Persisted status should be 'pending'"
        assert raw_workshop['signup_enabled'] is True, "Persisted signup_enabled should be True"
        
    finally:
        if os.path.exists(path):
            os.remove(path)
