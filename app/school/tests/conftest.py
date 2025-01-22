import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from core.models import User
from school.models import Clase, Student, Tutor, Atendance

"""Fixtures for the school app tests."""

@pytest.fixture
def api_client():
    """Fixture to create an APIClient instance."""
    return APIClient()

@pytest.fixture
def create_user():
    """Fixture to create a normal user."""
    return baker.make(User, first_name='John', last_name='Doe') 

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

@pytest.fixture
def create_clase():
    """Fixture to create a category for the authenticated user."""
    grade = '1'
    level = 'S'
    section = 'A'
    return baker.make(Clase, grade=grade, level=level, section=section)

@pytest.fixture
def create_student(create_clase):
    """Fixture to create a student"""
    return baker.make(Student, uid='46345643', clase=create_clase, first_name='Tom', last_name='Doe', tutor_phone='123456789')

@pytest.fixture
def create_tutor(create_user, create_student):
    """Fixture to create a tutor"""
    return baker.make(Tutor, user=create_user, students=[create_student], phone_number='123456789', address='Calle 123', email='tutor@tutor.com')

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