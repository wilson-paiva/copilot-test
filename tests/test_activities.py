"""
Tests for the GET /activities endpoint.
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """Test that GET /activities returns all available activities."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Verify all activities are present
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data
    assert "Soccer Practice" in data
    assert "Basketball Club" in data
    assert "Art Studio" in data
    assert "Drama Club" in data
    assert "Math Olympiad" in data
    assert "Science Club" in data


def test_get_activities_returns_correct_structure(client):
    """Test that each activity has the correct structure."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Test the structure of one activity
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)


def test_get_activities_participants_are_correct(client):
    """Test that participants list is properly populated."""
    response = client.get("/activities")
    
    assert response.status_code == 200
    data = response.json()
    
    # Check participants for Chess Club
    chess_club_participants = data["Chess Club"]["participants"]
    assert "michael@mergington.edu" in chess_club_participants
    assert "daniel@mergington.edu" in chess_club_participants
    
    # Check participants for Programming Class
    prog_class_participants = data["Programming Class"]["participants"]
    assert "emma@mergington.edu" in prog_class_participants
    assert "sophia@mergington.edu" in prog_class_participants
