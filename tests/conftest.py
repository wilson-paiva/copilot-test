"""
Pytest configuration and shared fixtures for FastAPI tests.
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    """
    Provides a TestClient for the FastAPI app.
    Each test gets a fresh client instance.
    """
    return TestClient(app)
