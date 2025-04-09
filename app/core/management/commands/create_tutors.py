# import random
# from datetime import timedelta
# from django.core.management.base import BaseCommand
# from django.utils import timezone
# from core.models import User
# from school.models import Student, Tutor, TutorAuthInfo

# class Command(BaseCommand):
#     help = 'Create tutors for every student'
#     def add_arguments(self, parser):
#         parser.add_argument(
#             '--school',
#             type=int,
#             required=True,
#             help='Specify the school ID to create tutors for'
#         )

#     def handle(self, *args, **options):
#         school = options['school']
#         # Get all students in the specified school
#         students = Student.objects.filter(school_id=school)
#         # loop into students
#         for student in students:
#             # Generate a random username and password
#             username = f"{student.first_name.lower()}.{student.last_name.lower()}."
#             password = f"password{random.randint(1000, 9999)}"
#             # Create a new tutor
#             tutor = Tutor.objects.create(
#                 first_name=student.first_name,
#                 last_name=student.last_name,
#                 school_id=school,
#                 student_id=student.id,
#                 created_at=timezone.now(),
#                 updated_at=timezone.now()
#             )
#             # Create an auth info for the tutor
#             TutorAuthInfo.objects.create(
#                 user=tutor,
#                 username=username,
#                 password=password,
#                 created_at=timezone.now(),
#                 updated_at=timezone.now()
#             )
#         pass