import pytest
from rest_framework import status
from school.models import Clase

@pytest.mark.django_db
class TestClase:
    """Tests for the Clase model."""

    def test_create_clase_anonymous_user_return_401(self, api_client):
        """Test creating a clase."""
        response = api_client.post("/api/clase/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_clase_authenticated_user_return_403(self, create_authenticate_user):
        """Test creating a clase."""
        response = create_authenticate_user.post("/api/clase/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_clase_admin_user_return_201(self, create_admin_user):
        """Test creating a clase."""
        payload = {
            "grade": "1",
            "level": "S",
            "section": "A",
        }
        response = create_admin_user.post("/api/clase/", payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_clase_anonymous_user_return_401(self, api_client):
        """Test getting a clase."""
        response = api_client.get("/api/clase/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_clase_authenticated_user_return_200(self, create_authenticate_user, create_clase):
        """Test getting a clase."""
        response = create_authenticate_user.get("/api/clase/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['grade'] == '1'
        assert response.json()[0]['level'] == 'S'
        assert response.json()[0]['section'] == 'A'

    def test_get_clase_admin_user_return_200(self, create_admin_user, create_clase):
        """Test getting a clase."""
        response = create_admin_user.get("/api/clase/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['grade'] == '1'
        assert response.json()[0]['level'] == 'S'
        assert response.json()[0]['section'] == 'A'

    def test_update_clase_anonymous_user_return_401(self, api_client, create_clase):
        """Test updating a clase."""
        payload = {
            "grade": "2",
            "level": "S",
            "section": "A",
        }
        response = api_client.put(f"/api/clase/{create_clase.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_clase_authenticated_user_return_403(self, create_authenticate_user, create_clase):
        """Test updating a clase."""
        payload = {
            "grade": "2",
            "level": "S",
            "section": "A",
        }
        response = create_authenticate_user.put(f"/api/clase/{create_clase.id}/", payload)
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_update_clase_admin_user_return_200(self, create_admin_user, create_clase):
        """Test updating a clase."""
        payload = {
            "grade": "2",
            "level": "S",
            "section": "A",
        }
        response = create_admin_user.put(f"/api/clase/{create_clase.id}/", payload)
        assert response.status_code == status.HTTP_200_OK
        assert response.json()['grade'] == '2'
        assert response.json()['level'] == 'S'
        assert response.json()['section'] == 'A'

    def test_delete_clase_anonymous_user_return_401(self, api_client, create_clase):
        """Test deleting a clase."""
        response = api_client.delete(f"/api/clase/{create_clase.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_clase_authenticated_user_return_403(self, create_authenticate_user, create_clase):
        """Test deleting a clase."""
        response = create_authenticate_user.delete(f"/api/clase/{create_clase.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_clase_admin_user_return_204(self, create_admin_user, create_clase):
        """Test deleting a clase."""
        response = create_admin_user.delete(f"/api/clase/{create_clase.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert Clase.objects.count() == 0