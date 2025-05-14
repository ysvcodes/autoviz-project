# tests/test_app.py
"""
Author: autoviz-project user
File Purpose: Unit tests for the autoviz-project application.
Dependencies: pytest, Flask (from app.main)
"""
import pytest
from app.main import app_instance # Import the Flask app instance

@pytest.fixture
def client():
    app_instance.config['TESTING'] = True
    with app_instance.test_client() as client:
        yield client

def test_home_status_code(client):
    """Test case 1: Check if the home page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200, "Home page should return status 200"

def test_home_data(client):
    """Test case 2: Check if the home page returns correct data."""
    response = client.get('/')
    assert b"Hello from autoviz-project (v2 pipeline)!" in response.data, "Home page should contain the greeting"

def test_always_passes():
    """A simple test that always passes, for pipeline verification."""
    assert True 