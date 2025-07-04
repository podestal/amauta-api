import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User
from school.models import Student, Tutor, TutorAuthInfo, School
import re

class Command(BaseCommand):
    help = 'Create tutors for every student'
    def add_arguments(self, parser):
        parser.add_argument(
            '--school',
            type=int,
            required=True,
            help='Specify the school ID to create tutors for'
        )

    def handle(self, *args, **options):
        school_id = options['school']
        school = School.objects.get(id=school_id)
        # Get all students in the specified school
        students = Student.objects.filter(school=school)
        # loop into students
        for student in students:
            if not student.tutor_phone:
                self.stdout.write(self.style.WARNING(
                    f'Student {student.first_name} {student.last_name} does not have a phone number'
                ))
                continue

            if Tutor.objects.filter(students=student, school=school).exists():
                self.stdout.write(self.style.WARNING(
                    f'Tutor already exists for {student.first_name} {student.last_name}'
                ))
                continue
            first_name = re.sub(r"\s+", "", student.first_name)
            last_name = re.sub(r"\s+", "", student.last_name.lower().split(' ')[0])
            slicer = 1
            # Generate a random username and password
            username = f"{first_name.lower()[:slicer]}{last_name.lower().split(' ')[0]}"
            password = f"{last_name}{student.dni[:4]}"

            self.stdout.write(self.style.SUCCESS(
                f'Creating tutor for {first_name} {last_name} with username: {username} and password: {password}'
            ))


            # check if the username already exists
            duplicatedUser = User.objects.filter(username=username).exists()

            while duplicatedUser:
                self.stdout.write(self.style.SUCCESS(
                    f'Username {username} already exists, generating a new one'
                ))
                slicer += 1
                username = f"{first_name.lower()[:slicer]}{last_name}"
                duplicatedUser = User.objects.filter(username=username).exists()

            username = re.sub(r"\s+", "", username)
            password = re.sub(r"\s+", "", password)
            # Create a new user
            user = User.objects.create_user(
                username=username,
                password=password,
                profile="tutor",
                first_name='',
                last_name='',
                profile='tutor',
                email = f"{first_name.lower().split(' ')[0]}{random.randint(1000000000, 9999999999)}@amautapp.com",
            )

            # Create a new auth info for the user
            TutorAuthInfo.objects.create(
                username=username,
                password=password,
                school=school,
                student=student,
                created_at=timezone.now(),
            )

            # Create a new tutor
            tutor = Tutor.objects.create(
                user=user,
                school=school,
            )

            tutor.students.set([student])

            self.stdout.write(self.style.SUCCESS(
                f'Tutor created for {first_name} {last_name} with username: {username} and password: {password}'
            ))
        self.stdout.write(self.style.SUCCESS(   
            'Tutors created successfully'
        ))