import pytest
from rest_framework import status
from model_bakery import baker
from school.models import Instructor, Clase

@pytest.fixture
def create_clase():
    """Fixture to create a category for the authenticated user."""
    grade = '1'
    level = 'S'
    section = 'A'
    return baker.make(Clase, grade=grade, level=level, section=section)

@pytest.fixture
def create_instructor(create_clase, create_user):
    """Fixture to create a instructor"""
    return baker.make(Instructor, clases=[create_clase], user=create_user)

@pytest.mark.django_db
class TestInstructor:

    def test_create_instructor_anonymous_user_return_401(self, api_client):
        """Test creating a instructor."""
        response = api_client.post("/api/instructor/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_instructor_authenticated_user_return_403(self, create_authenticate_user):
        """Test creating a instructor."""
        response = create_authenticate_user.post("/api/instructor/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_create_instructor_admin_user_return_201(self, create_admin_user, create_user ,create_clase):
        """Test creating a instructor."""
        payload = {
            "user": create_user.id,
            "clases": create_clase.id,
            "first_name": "John",
            "last_name": "Doe"
        }
        response = create_admin_user.post("/api/instructor/", payload)
        assert response.status_code == status.HTTP_201_CREATED

    def test_get_instructor_anonymous_user_return_401(self, api_client):
        """Test getting a instructor."""
        response = api_client.get("/api/instructor/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_instructor_authenticated_user_return_200(self, create_authenticate_user, create_instructor):
        """Test getting a instructor."""
        response = create_authenticate_user.get("/api/instructor/")
        print('response', response.json())
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['first_name'] == 'John'
        assert response.json()[0]['last_name'] == 'Doe'

    def test_get_instructor_admin_user_return_200(self, create_admin_user, create_instructor):
        """Test getting a instructor."""
        response = create_admin_user.get("/api/instructor/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['first_name'] == 'John'
        assert response.json()[0]['last_name'] == 'Doe'

    def test_update_instructor_anonymous_user_return_401(self, api_client, create_instructor):
        """Test updating a instructor."""
        payload = {
            "user": create_instructor.user.id,
            "clases": create_instructor.clases.first().id,
            "first_name": "Jane",
            "last_name": "Doe"
        }
        response = api_client.put(f"/api/instructor/{create_instructor.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_instructor_authenticated_user_return_200(self, create_authenticate_user, create_instructor):
        """Test updating a instructor."""
        payload = {
            "user": create_instructor.user.id,
            "clases": create_instructor.clases.first().id,
            "first_name": "Jane",
            "last_name": "Doe"
        }
        response = create_authenticate_user.put(f"/api/instructor/{create_instructor.id}/", payload)
        assert response.status_code == status.HTTP_200_OK

    def test_update_instructor_admin_user_return_200(self, create_admin_user, create_instructor):
        """Test updating a instructor."""
        payload = {
            "user": create_instructor.user.id,
            "clases": create_instructor.clases.first().id,
            "first_name": "Jane",
            "last_name": "Doe"
        }
        response = create_admin_user.put(f"/api/instructor/{create_instructor.id}/", payload)
        assert response.status_code == status.HTTP_200_OK

    def test_delete_instructor_anonymous_user_return_401(self, api_client, create_instructor):
        """Test deleting a instructor."""
        response = api_client.delete(f"/api/instructor/{create_instructor.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_delete_instructor_authenticated_user_return_403(self, create_authenticate_user, create_instructor):
        """Test deleting a instructor."""
        response = create_authenticate_user.delete(f"/api/instructor/{create_instructor.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_instructor_admin_user_return_204(self, create_admin_user, create_instructor):
        """Test deleting a instructor."""
        response = create_admin_user.delete(f"/api/instructor/{create_instructor.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT