import pytest
from datetime import date
from rest_framework import status
from model_bakery import baker
from school.models import Atendance, Student, Clase

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

@pytest.fixture
def create_clase():
    """Fixture to create a category for the authenticated user."""
    grade = '1'
    level = 'S'
    section = 'A'
    return baker.make(Clase, grade=grade, level=level, section=section)

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

    def test_by_classroom_without_query_param_return_400(self, create_authenticate_user):
        """
        Test the byClassroom method when the 'classroom' query parameter is missing.
        """
        response = create_authenticate_user.get("/api/atendance/byClassroom/")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json() == {"error": "Classroom parameter is required"}

    def test_by_classroom_with_valid_data(self, create_authenticate_user, create_clase):
        """
        Test the byClassroom method with valid classroom and today's date.
        """

        student1 = baker.make(Student, uid='46345643', first_name='Tom', last_name='Doe', tutor_phone='123456789', clase=create_clase)
        student2 = baker.make(Student, uid='46345644', first_name='John', last_name='Doe', tutor_phone='123456789', clase=create_clase)
        other_clase = baker.make(Clase, grade='3', level='S', section='A')
        other_student = baker.make(Student, uid='46345645', first_name='Jane', last_name='Doe', tutor_phone='123456789', clase=other_clase)
        attendance1 = baker.make(Atendance, student=student1, status='O', kind='I', attendance_type='A', created_by='Manuel Doe')
        attendance2 = baker.make(Atendance, student=student2, status='O', kind='I', attendance_type='A', created_by='Manuel Doe')
        baker.make(Atendance, student=other_student, status='O', kind='I', attendance_type='A', created_by='Manuel Doe') 

        response = create_authenticate_user.get(f"/api/atendance/byClassroom/?classroom={create_clase.id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 2
        assert response.json()[0]['student'] == int(student1.uid)
        assert response.json()[1]['student'] == int(student2.uid)


    def test_by_classroom_with_no_results(self, create_authenticate_user, create_clase):
        """
        Test the byClassroom method when no attendances match the given classroom and date.
        """

        clase = baker.make(Clase, grade='3', level='S', section='A')
        baker.make(Student, clase=clase)
        baker.make(Atendance, status='O', kind='I', attendance_type='A', created_by='Manuel Doe')

        response = create_authenticate_user.get(f"/api/atendance/byClassroom/?classroom={create_clase.id}")

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

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
