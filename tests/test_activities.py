"""Tests for the GET /activities endpoint."""

import pytest


def test_get_activities_success(client):
    """Test successfully retrieving all activities."""
    response = client.get("/activities")
    assert response.status_code == 200
    
    activities = response.json()
    assert isinstance(activities, dict)
    assert len(activities) > 0


def test_activities_response_structure(client):
    """Test that each activity has the required fields."""
    response = client.get("/activities")
    activities = response.json()
    
    # Check each activity has required fields
    for activity_name, activity_data in activities.items():
        assert isinstance(activity_name, str)
        assert "description" in activity_data
        assert "schedule" in activity_data
        assert "max_participants" in activity_data
        assert "participants" in activity_data
        
        # Verify field types
        assert isinstance(activity_data["description"], str)
        assert isinstance(activity_data["schedule"], str)
        assert isinstance(activity_data["max_participants"], int)
        assert isinstance(activity_data["participants"], list)


def test_activities_have_participants(client):
    """Test that activities have participant lists."""
    response = client.get("/activities")
    activities = response.json()
    
    # At least one activity should have participants
    has_participants = any(
        len(activity["participants"]) > 0 
        for activity in activities.values()
    )
    assert has_participants, "At least one activity should have participants"


def test_activities_contains_chess_club(client):
    """Test that Chess Club is in the activities list."""
    response = client.get("/activities")
    activities = response.json()
    
    assert "Chess Club" in activities
    chess_club = activities["Chess Club"]
    assert chess_club["max_participants"] > 0
    assert isinstance(chess_club["participants"], list)
