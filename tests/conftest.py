"""Pytest configuration and shared fixtures for API tests."""

import pytest
from copy import deepcopy
from fastapi.testclient import TestClient
from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset the activities dictionary to its original state before each test."""
    # Store original state
    original_state = deepcopy(app_module.activities)
    
    yield
    
    # Reset activities to original state after test
    app_module.activities.clear()
    app_module.activities.update(original_state)


@pytest.fixture
def client():
    """Provide a TestClient for making requests to the FastAPI app."""
    return TestClient(app_module.app)


@pytest.fixture
def sample_activity():
    """Provide a sample activity name for testing."""
    return "Chess Club"


@pytest.fixture
def sample_email():
    """Provide a sample student email for testing."""
    return "test.student@mergington.edu"


@pytest.fixture
def existing_email():
    """Provide an email already registered in an activity."""
    return "michael@mergington.edu"

