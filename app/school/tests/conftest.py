import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from core.models import User

"""Fixtures for the school app tests."""

@pytest.fixture
def api_client():
    """Fixture to create an APIClient instance."""
    return APIClient()

@pytest.fixture
def create_user():
    """Fixture to create a normal user."""
    return baker.make(User) 

@pytest.fixture
def create_authenticate_user(api_client, create_user):
    """Fixture to authenticate a normal user."""
    api_client.force_authenticate(user=create_user)
    return api_client

@pytest.fixture
def create_admin_user(api_client):
    """Fixture to authenticate an admin user."""
    admin_user = baker.make(User, is_staff=True)
    api_client.force_authenticate(user=admin_user)
    return api_client


