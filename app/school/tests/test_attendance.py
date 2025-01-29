import pytest
from django.utils import timezone
from rest_framework import status
from model_bakery import baker
from school.models import Atendance, Student, Clase, Tutor
from datetime import datetime

@pytest.fixture
def create_tutor(create_student):
    """Fixture to create a tutor."""
    return baker.make(Tutor, students=[create_student], first_name='John', last_name='Doe', phone_number='123456789')

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
        
    def test_create_atendance_student_not_found(self, create_authenticate_user):
        """Test creating an attendance when the student is not found."""
        payload = {
            "student": 13564,
            "status": "O",
            "attendance_type": "A",
            "kind": "I",
            "created_by": "John Doe",
        }
        response = create_authenticate_user.post("/api/atendance/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "No se pudo encontrar alumno"}

    def test_create_atendance_student_already_scanned_twice(self, create_authenticate_user, create_student):
        """Test creating an attendance when the student has already been scanned twice today."""
        baker.make(Atendance, student=create_student, created_at=timezone.now())
        baker.make(Atendance, student=create_student, created_at=timezone.now())
        payload = {
            "student": create_student.uid,
            "status": "O",
            "attendance_type": "A",
            "kind": "I",
            "created_by": "John Doe",
        }
        response = create_authenticate_user.post("/api/atendance/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Alumno ya fué escaneado"}

    def test_create_atendance_student_already_scanned_once_kind_I(self, create_authenticate_user, create_student):
        """Test creating an attendance when the student has already been scanned once today and the kind is 'I'."""
        baker.make(Atendance, student=create_student, created_at=timezone.now())
        payload = {
            "student": create_student.uid,
            "status": "O",
            "attendance_type": "A",
            "kind": "I",
            "created_by": "John Doe",
        }
        response = create_authenticate_user.post("/api/atendance/", payload)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Alumno ya fué escaneado"}

    def test_create_atendance_status_not_tutor_found(self, create_authenticate_user, create_student, create_tutor):
        """Test creating an attendance when the status is not 'O' and the tutor is found."""
        payload = {
            "student": create_student.uid,
            "status": "N",
            "attendance_type": "A",
            "kind": "I",
            "created_by": "John Doe",
        }
        response = create_authenticate_user.post("/api/atendance/", payload)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()['status'] == 'N'
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

    def test_by_classroom_with_week_filter(self, create_authenticate_user, create_clase, create_atendance):
        """Test the byClassroom method with the classroom parameter and week filter."""
        week = create_atendance.created_at.isocalendar()[1]
        response = create_authenticate_user.get(f"/api/atendance/byClassroom/?classroom={create_clase.id}&week={week}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]['student'] == int(create_atendance.student.uid)

    def test_by_classroom_with_day_and_month_filter(self, create_authenticate_user, create_clase, create_atendance):
        """Test the byClassroom method with the classroom parameter and day and month filter."""
        response = create_authenticate_user.get(f"/api/atendance/byClassroom/?classroom={create_clase.id}&day={datetime.now().day}&month={datetime.now().month}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]['student'] == int(create_atendance.student.uid)

    def test_by_classroom_with_month_filter(self, create_authenticate_user, create_clase, create_atendance):
        """Test the byClassroom method with the classroom parameter and month filter."""
        response = create_authenticate_user.get(f"/api/atendance/byClassroom/?classroom={create_clase.id}&month={datetime.now().month}")
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert response.json()[0]['student'] == int(create_atendance.student.uid)

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
        assert response.status_code == status.HTTP_200_OK
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
        assert response.status_code == status.HTTP_200_OK
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
