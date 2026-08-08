"""Tests for the POST /activities/{activity_name}/unregister endpoint."""

import pytest


def test_unregister_success(client, sample_activity, existing_email):
    """Test successful unregister from an activity."""
    response = client.post(
        f"/activities/{sample_activity}/unregister",
        params={"email": existing_email}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert existing_email in data["message"]
    assert sample_activity in data["message"]


def test_unregister_removes_participant(client, sample_activity, existing_email):
    """Test that unregister actually removes the participant."""
    # Get initial participant list
    activities_response = client.get("/activities")
    initial_participants = activities_response.json()[sample_activity]["participants"].copy()
    initial_count = len(initial_participants)
    
    # Unregister
    client.post(
        f"/activities/{sample_activity}/unregister",
        params={"email": existing_email}
    )
    
    # Get updated participant list
    activities_response = client.get("/activities")
    updated_participants = activities_response.json()[sample_activity]["participants"]
    
    # Verify the email was removed
    assert existing_email not in updated_participants
    assert len(updated_participants) == initial_count - 1


def test_unregister_activity_not_found(client, existing_email):
    """Test unregister fails when activity doesn't exist."""
    response = client.post(
        "/activities/NonexistentClub/unregister",
        params={"email": existing_email}
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_unregister_not_registered(client, sample_activity, sample_email):
    """Test unregister fails when student is not registered."""
    response = client.post(
        f"/activities/{sample_activity}/unregister",
        params={"email": sample_email}
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "not registered" in data["detail"].lower()


def test_unregister_response_format(client, sample_activity, existing_email):
    """Test that unregister response has correct format."""
    response = client.post(
        f"/activities/{sample_activity}/unregister",
        params={"email": existing_email}
    )
    
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)


def test_signup_then_unregister(client, sample_activity, sample_email):
    """Test signing up and then unregistering from an activity."""
    # Sign up
    signup_response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    assert signup_response.status_code == 200
    
    # Verify participant was added
    activities_response = client.get("/activities")
    participants = activities_response.json()[sample_activity]["participants"]
    assert sample_email in participants
    
    # Unregister
    unregister_response = client.post(
        f"/activities/{sample_activity}/unregister",
        params={"email": sample_email}
    )
    assert unregister_response.status_code == 200
    
    # Verify participant was removed
    activities_response = client.get("/activities")
    participants = activities_response.json()[sample_activity]["participants"]
    assert sample_email not in participants
