"""
Tests for the POST /activities/{activity_name}/signup endpoint.
"""

import pytest


def test_successful_signup(client):
    """Test successfully signing up a student for an activity."""
    response = client.post(
        "/activities/Chess%20Club/signup?email=newstudent@mergington.edu"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Signed up" in data["message"]
    assert "newstudent@mergington.edu" in data["message"]
    assert "Chess Club" in data["message"]


def test_signup_adds_participant_to_activity(client):
    """Test that signup actually adds the participant to the activity."""
    email = "testuser@mergington.edu"
    
    # Sign up the user
    response = client.post(
        "/activities/Basketball%20Club/signup?email=" + email
    )
    assert response.status_code == 200
    
    # Verify the participant was added
    activities_response = client.get("/activities")
    activities = activities_response.json()
    assert email in activities["Basketball Club"]["participants"]


def test_signup_nonexistent_activity_returns_404(client):
    """Test that signing up for a non-existent activity returns 404."""
    response = client.post(
        "/activities/Nonexistent%20Activity/signup?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_signup_duplicate_registration_returns_400(client):
    """Test that signing up twice for the same activity returns 400."""
    email = "duplicate@mergington.edu"
    activity = "Chess%20Club"
    
    # First signup should succeed
    response1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response1.status_code == 200
    
    # Second signup should fail
    response2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert response2.status_code == 400
    data = response2.json()
    assert "already signed up" in data["detail"]


def test_signup_already_existing_participant_returns_400(client):
    """Test that trying to sign up an already existing participant returns 400."""
    # michael@mergington.edu is already signed up for Chess Club
    response = client.post(
        "/activities/Chess%20Club/signup?email=michael@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "already signed up" in data["detail"]
