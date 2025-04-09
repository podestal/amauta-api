import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from core.models import User
from school.models import Student, Tutor, TutorAuthInfo, School

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
            if student.tutor_phone:
                continue
            student.tutor_phone = random.randint(1000000000, 9999999999)
            student.save()
            self.stdout.write(self.style.SUCCESS(
                f'Creating tutor for {student.first_name} {student.last_name} with phone: {student.tutor_phone}'
            ))

