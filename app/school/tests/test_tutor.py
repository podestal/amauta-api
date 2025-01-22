import pytest
from rest_framework import status

@pytest.mark.django_db
class TestTutor:

    def test_create_tutor_anonymous_user_return_401(self, api_client):
        """Test creating a tutor."""
        response = api_client.post("/api/tutor/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_tutor_authenticated_user_return_403(self, create_authenticate_user):
        """Test creating a tutor."""
        response = create_authenticate_user.post("/api/tutor/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_tutor_admin_user_return_201(self, create_admin_user, create_user, create_student):
        print('create_student', create_student)
        """Test creating a tutor."""
        payload = {
            "user": create_user.id,
            "students": [create_student.uid],
            "phone_number": "123456789",
            "address": "Calle 123",
            "email": "tutor@tutor.com"
        }
        response = create_admin_user.post("/api/tutor/", payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_tutor_anonymous_user_return_401(self, api_client):
        """Test getting a tutor."""
        response = api_client.get("/api/tutor/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_tutor_authenticated_user_return_200(self, create_authenticate_user, create_tutor):
        """Test getting a tutor."""
        response = create_authenticate_user.get("/api/tutor/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['phone_number'] == '123456789'
        assert response.json()[0]['address'] == 'Calle 123'

    def test_get_tutor_admin_user_return_200(self, create_admin_user, create_tutor):
        """Test getting a tutor."""
        response = create_admin_user.get("/api/tutor/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['phone_number'] == '123456789'
        assert response.json()[0]['address'] == 'Calle 123'

    def test_update_tutor_anonymous_user_return_401(self, api_client, create_tutor):
        """Test updating a tutor."""
        payload = {
            "user": create_tutor.user.id,
            "students": [create_tutor.students.first().uid],
            "phone_number": "987654321",
            "address": "Calle 321",
            "email": "tutor@tutor.com",
        }
        response = api_client.put(f"/api/tutor/{create_tutor.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_tutor_authenticated_user_return_200(self, create_authenticate_user, create_tutor):
        """Test updating a tutor."""
        payload = {
            "user": create_tutor.user.id,
            "students": [create_tutor.students.first().uid],
            "phone_number": "987654321",
            "address": "Calle 321",
            "email":  "tutor@tutor.com",
        }
        response = create_authenticate_user.patch(f"/api/tutor/{create_tutor.id}/", payload)
        assert response.status_code == status.HTTP_200_OK

    def test_update_tutor_admin_user_return_200(self, create_admin_user, create_tutor):
        """Test updating a tutor."""
        payload = {
            "can_access": True,
            "phone_number": "987654321",
            "address": "Calle 321",
            "email": "tutor@tutor.com",
        }
        response = create_admin_user.patch(f"/api/tutor/{create_tutor.id}/", payload)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_tutor_anonymous_user_return_401(self, api_client, create_tutor):
        """Test deleting a tutor."""
        response = api_client.delete(f"/api/tutor/{create_tutor.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_tutor_authenticated_user_return_403(self, create_authenticate_user, create_tutor):
        """Test deleting a tutor."""
        response = create_authenticate_user.delete(f"/api/tutor/{create_tutor.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_tutor_admin_user_return_204(self, create_admin_user, create_tutor):
        """Test deleting a tutor."""
        response = create_admin_user.delete(f"/api/tutor/{create_tutor.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    

    