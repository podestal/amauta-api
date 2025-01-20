import pytest
from rest_framework import status
from model_bakery import baker
from school.models import Atendance, Student

@pytest.fixture
def create_student():
    """Fixture to create a student."""
    return baker.make(Student, uid='46345643', first_name='Tom', last_name='Doe', tutor_phone='123456789')

@pytest.fixture
def create_atendance(create_student):
    """Fixture to create a atendance."""
    return baker.make(Atendance, 
                student=create_student, 
                status='O', 
                created_by='John Doe', 
                observations='Observations', 
                attendance_type='A',
                kind='I')

@pytest.mark.django_db
class TestAtendance:

    def test_create_atendance_anonymous_user_return_401(self, api_client):
        """Test creating a atendance."""
        response = api_client.post("/api/atendance/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_create_atendance_authenticated_user_return_201(self, create_authenticate_user, create_student):
        """Test creating a atendance."""
        payload = {
            "student": create_student.uid,
            "status": "O",
            "attendance_type": "A",
            "kind": "I",
            "created_by": "John Doe",
        }
        response = create_authenticate_user.post("/api/atendance/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['status'] == 'O'
        assert response.json()['kind'] == 'I'
        assert response.json()['created_by'] == 'John Doe'

    def test_create_atendance_admin_user_return_201(self, create_admin_user, create_student):
        """Test creating a atendance."""
        payload = {
            "student": create_student.uid,
            "status": "O",
            "attendance_type": "A",
            "kind": "I",
            "created_by": "John Doe",
        }
        response = create_admin_user.post("/api/atendance/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['status'] == 'O'
        assert response.json()['kind'] == 'I'
        assert response.json()['created_by'] == 'John Doe'

    def test_get_atendance_anonymous_user_return_401(self, api_client):
        """Test getting a atendance."""
        response = api_client.get("/api/atendance/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_atendance_authenticated_user_return_200(self, create_authenticate_user, create_atendance):
        """Test getting a atendance."""
        response = create_authenticate_user.get("/api/atendance/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['status'] == 'O'
        assert response.json()[0]['kind'] == 'I'
        assert response.json()[0]['created_by'] == 'John Doe'

    def test_get_atendance_admin_user_return_200(self, create_admin_user, create_atendance):
        """Test getting a atendance."""
        response = create_admin_user.get("/api/atendance/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()[0]['status'] == 'O'
        assert response.json()[0]['kind'] == 'I'
        assert response.json()[0]['created_by'] == 'John Doe'

    def test_update_atendance_anonymous_user_return_401(self, api_client, create_atendance):
        """Test updating a atendance."""
        payload = {
            "status": "L",
        }
        response = api_client.patch(f"/api/atendance/{create_atendance.id}/", payload)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_update_atendance_authenticated_user_return_200(self, create_authenticate_user, create_atendance):
        """Test updating a atendance."""
        payload = {
            "status": "L",
            "kind": "O",
            "student": create_atendance.student.uid,
        }
        response = create_authenticate_user.patch(f"/api/atendance/{create_atendance.id}/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['status'] == 'L'
        assert response.json()['kind'] == 'O'

    def test_update_atendance_admin_user_return_200(self, create_admin_user, create_atendance):
        """Test updating a atendance."""
        payload = {
            "status": "L",
            "kind": "O",
            "student": create_atendance.student.uid,
        }
        response = create_admin_user.patch(f"/api/atendance/{create_atendance.id}/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['status'] == 'L'
        assert response.json()['kind'] == 'O'

    def test_delete_atendance_anonymous_user_return_401(self, api_client, create_atendance):
        """Test deleting a atendance."""
        response = api_client.delete(f"/api/atendance/{create_atendance.id}/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_atendance_authenticated_user_return_204(self, create_authenticate_user, create_atendance):
        """Test deleting a atendance."""
        response = create_authenticate_user.delete(f"/api/atendance/{create_atendance.id}/")
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_delete_atendance_admin_user_return_204(self, create_admin_user, create_atendance):
        """Test deleting a atendance."""
        response = create_admin_user.delete(f"/api/atendance/{create_atendance.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT
