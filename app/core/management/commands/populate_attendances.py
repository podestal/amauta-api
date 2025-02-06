import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from school.models import Atendance, Student

class Command(BaseCommand):
    help = 'Populate attendances for all students'

    def handle(self, *args, **options):
        STATUS_CHOICES_OUT = ['O', 'E', 'T']
        STATUS_CHOICES_IN = ['L', 'O', 'N']
        TYPE_CHOICES = ['A', 'M']

        # Get all students
        students = Student.objects.all()

        if not students.exists():
            print("No students found in the database.")
            return


        start_date = timezone.datetime(timezone.now().year, 1, 1, tzinfo=timezone.get_current_timezone())
        end_date = timezone.now()

        delta = end_date - start_date

        attendances_created = 0

        for student in students:
            for i in range(delta.days + 1): 
                date = start_date + timedelta(days=i)
                
                status_in = random.choice(STATUS_CHOICES_IN)
                status_out = random.choice(STATUS_CHOICES_OUT)
                attendance_type = random.choice(TYPE_CHOICES)

                Atendance.objects.create(
                    created_at=date,
                    updated_at=date,
                    status=status_in,
                    attendance_type=attendance_type,
                    student=student,
                    created_by="System",
                    observations="Generated automatically",
                    kind="I",
                )

                if status_in != 'N':
                    Atendance.objects.create(
                        created_at=date,
                        updated_at=date,
                        status=status_out,
                        attendance_type=attendance_type,
                        student=student,
                        created_by="System",
                        observations="Generated automatically",
                        kind="O",
                    )

                attendances_created += 2

        self.stdout.write(self.style.SUCCESS(f'{attendances_created} attendances created successfully.'))