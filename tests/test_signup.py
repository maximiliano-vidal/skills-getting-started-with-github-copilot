"""Tests for the POST /activities/{activity_name}/signup endpoint."""

import pytest


def test_signup_success(client, sample_activity, sample_email):
    """Test successful signup for an activity."""
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 200
    
    data = response.json()
    assert "message" in data
    assert sample_email in data["message"]
    assert sample_activity in data["message"]


def test_signup_adds_participant(client, sample_activity, sample_email):
    """Test that signup actually adds the participant to the activity."""
    # Get initial participant count
    activities_response = client.get("/activities")
    initial_participants = activities_response.json()[sample_activity]["participants"].copy()
    
    # Sign up
    client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    # Get updated participant list
    activities_response = client.get("/activities")
    updated_participants = activities_response.json()[sample_activity]["participants"]
    
    # Verify the new email was added
    assert sample_email in updated_participants
    assert len(updated_participants) == len(initial_participants) + 1


def test_signup_activity_not_found(client, sample_email):
    """Test signup fails when activity doesn't exist."""
    response = client.post(
        "/activities/NonexistentClub/signup",
        params={"email": sample_email}
    )
    assert response.status_code == 404
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"].lower()


def test_signup_duplicate_email(client, sample_activity, existing_email):
    """Test signup fails when student already signed up."""
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": existing_email}
    )
    assert response.status_code == 400
    
    data = response.json()
    assert "detail" in data
    assert "already" in data["detail"].lower()


def test_signup_response_format(client, sample_activity, sample_email):
    """Test that signup response has correct format."""
    response = client.post(
        f"/activities/{sample_activity}/signup",
        params={"email": sample_email}
    )
    
    assert response.headers["content-type"] == "application/json"
    data = response.json()
    assert isinstance(data, dict)
    assert "message" in data
    assert isinstance(data["message"], str)
