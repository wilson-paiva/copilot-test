"""
Tests for the DELETE /activities/{activity_name}/unregister endpoint.
"""

import pytest


def test_successful_unregister(client):
    """Test successfully unregistering a student from an activity."""
    # First, sign up a student
    email = "unregister_test@mergington.edu"
    signup_response = client.post(
        "/activities/Chess%20Club/signup?email=" + email
    )
    assert signup_response.status_code == 200
    
    # Then unregister the student
    response = client.delete(
        f"/activities/Chess%20Club/unregister?email={email}"
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "Unregistered" in data["message"]
    assert email in data["message"]
    assert "Chess Club" in data["message"]


def test_unregister_removes_participant_from_activity(client):
    """Test that unregister actually removes the participant from the activity."""
    email = "removal_test@mergington.edu"
    
    # Sign up the user
    client.post("/activities/Gym%20Class/signup?email=" + email)
    
    # Verify participant is in the list
    activities = client.get("/activities").json()
    assert email in activities["Gym Class"]["participants"]
    
    # Unregister the user
    client.delete(f"/activities/Gym%20Class/unregister?email={email}")
    
    # Verify participant is removed
    activities = client.get("/activities").json()
    assert email not in activities["Gym Class"]["participants"]


def test_unregister_nonexistent_activity_returns_404(client):
    """Test that unregistering from a non-existent activity returns 404."""
    response = client.delete(
        "/activities/Nonexistent%20Activity/unregister?email=student@mergington.edu"
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Activity not found" in data["detail"]


def test_unregister_nonexistent_participant_returns_400(client):
    """Test that unregistering a non-existent participant returns 400."""
    response = client.delete(
        "/activities/Chess%20Club/unregister?email=notregistered@mergington.edu"
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "not signed up" in data["detail"]


def test_unregister_existing_participant_returns_400_after_removal(client):
    """Test that trying to unregister an already unregistered participant returns 400."""
    email = "double_unregister_test@mergington.edu"
    
    # Sign up and then unregister
    client.post("/activities/Soccer%20Practice/signup?email=" + email)
    response1 = client.delete(
        f"/activities/Soccer%20Practice/unregister?email={email}"
    )
    assert response1.status_code == 200
    
    # Try to unregister again (should fail)
    response2 = client.delete(
        f"/activities/Soccer%20Practice/unregister?email={email}"
    )
    assert response2.status_code == 400
    data = response2.json()
    assert "not signed up" in data["detail"]
