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
