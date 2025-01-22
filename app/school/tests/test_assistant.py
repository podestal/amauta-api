import pytest
from rest_framework import status
from school.models import Assistant

@pytest.mark.django_db
class TestAssistant:

    def test_create_assistant_anonymous_user_return_401(self, api_client):
        """Test creating a assistant."""
        response = api_client.post("/api/assistant/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_assistant_authenticated_user_return_403(self, create_authenticate_user):
        """Test creating a assistant."""
        response = create_authenticate_user.post("/api/assistant/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_create_assistant_admin_user_return_201(self, create_admin_user, create_user):
        """Test creating a assistant."""
        payload = {
            "user": create_user.id,
            "first_name": "John",
            "last_name": "Doe",
            'phone_number': '123456789',
            'email': 'asistant@assistant.com',
            'address': 'Calle 123',

        }
        response = create_admin_user.post("/api/assistant/", payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_assistant_anonymous_user_return_401(self, api_client):
        """Test getting a assistant."""
        response = api_client.get("/api/assistant/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_assistant_authenticated_user_return_200(self, create_authenticate_user, create_assistant):
        """Test getting a assistant."""
        response = create_authenticate_user.get("/api/assistant/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['first_name'] == 'John'
        assert response.json()[0]['last_name'] == 'Doe'

    def test_get_assistant_admin_user_return_200(self, create_admin_user, create_assistant):
        """Test getting a assistant."""
        response = create_admin_user.get("/api/assistant/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['first_name'] == 'John'
        assert response.json()[0]['last_name'] == 'Doe'

    def test_me_authenticated_user_with_assistant(self, create_authenticate_user, create_user, create_assistant):
        """Test the me endpoint with an authenticated user who has an associated assistant."""
        response = create_authenticate_user.get("/api/assistant/me/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['user'] == create_user.id

    def test_me_authenticated_user_without_assistant(self, create_authenticate_user, create_user):
        """Test the me endpoint with an authenticated user who does not have an associated assistant."""
        response = create_authenticate_user.get("/api/assistant/me/")
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json() == {"error": "Assistant not found for the current user"}

    def test_me_unauthenticated_user(self, api_client):
        """Test the me endpoint with an unauthenticated user."""
        response = api_client.get("/api/assistant/me/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_assistant_anonymous_user_return_401(self, api_client, create_assistant):
        """Test updating a assistant."""
        payload = {
            "first_name": "Jane",
        }
        response = api_client.patch(f"/api/assistant/{create_assistant.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_assistant_authenticated_user_return_200(self, create_authenticate_user, create_assistant):
        """Test updating a assistant."""
        payload = {
            "first_name": "Jane",
        }
        response = create_authenticate_user.patch(f"/api/assistant/{create_assistant.id}/", payload)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_assistant_anonymous_user_return_401(self, api_client, create_assistant):
        """Test deleting a assistant."""
        response = api_client.delete(f"/api/assistant/{create_assistant.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_assistant_authenticated_user_return_403(self, create_authenticate_user, create_assistant):
        """Test deleting a assistant."""
        response = create_authenticate_user.delete(f"/api/assistant/{create_assistant.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_assistant_admin_user_return_204(self, create_admin_user, create_assistant):
        """Test deleting a assistant."""
        response = create_admin_user.delete(f"/api/assistant/{create_assistant.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT