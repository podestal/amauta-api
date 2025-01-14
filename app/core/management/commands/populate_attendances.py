import random
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from school.models import Atendance, Student

class Command(BaseCommand):
    help = 'Populate attendances for all students'

    def handle(self, *args, **options):
        STATUS_CHOICES = ['O', 'L', 'N', 'E', 'T']
        TYPE_CHOICES = ['A', 'M']

        # Get all students
        students = Student.objects.all()

        if not students.exists():
            print("No students found in the database.")
            return

        # Get the start date (January 1 of this year)
        start_date = datetime(datetime.now().year, 1, 1)
        # Get today's date
        end_date = datetime.now()

        # Calculate the date range
        delta = end_date - start_date

        attendances_created = 0

        # Loop through each student and each day in the range
        for student in students:
            for i in range(delta.days + 1):  # +1 to include today's date
                date = start_date + timedelta(days=i)
                
                # Randomly assign a status and type for attendance
                status = random.choice(STATUS_CHOICES)
                attendance_type = random.choice(TYPE_CHOICES)

                # Create attendance record
                Atendance.objects.create(
                    created_at=date,
                    updated_at=date,
                    status=status,
                    attendance_type=attendance_type,
                    student=student,
                    created_by="System",
                    observations="Generated automatically"
                )

                attendances_created += 1

        self.stdout.write(self.style.SUCCESS(f'{attendances_created} attendances created successfully.'))