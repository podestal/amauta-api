from django.core.management.base import BaseCommand
from django.utils import timezone
from school.models import Atendance, Student
import datetime

class Command(BaseCommand):
    help = 'Populate missing exit attendances for students with valid entrance attendance'

    def add_arguments(self, parser):
        parser.add_argument(
            '--date',
            type=str,
            help='Specify the date in YYYY-MM-DD format. Defaults to today.'
        )

    def handle(self, *args, **options):
        # Parse the date argument or use today's date
        if options['date']:
            try:
                attendance_date = datetime.datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD.'))
                return
        else:
            attendance_date = timezone.localdate()

        self.stdout.write(self.style.SUCCESS(f'Processing attendances for: {attendance_date}'))

        # Get all "I" (Entrance) attendances for the given date
        entrance_attendances = Atendance.objects.filter(
            created_at__date=attendance_date,
            kind="I"
        )

        created_count = 0  # Counter for created attendances

        for attendance in entrance_attendances:
            student = attendance.student
            
            # Check if the status is NOT "N" (Not Attended)
            if attendance.status == "E":
                # Check if the student already has an "O" (Exit) attendance for the same date
                if not Atendance.objects.filter(
                    student=student,
                    created_at__date=attendance_date,
                    kind="O"
                ).exists():
                    # Create exit attendance
                    Atendance.objects.create(
                        created_at=attendance_date,
                        updated_at=attendance_date,
                        status="E",  # On Time
                        attendance_type="M",  # Manual
                        student=student,
                        created_by="System",
                        observations="Automatically marked as checked out",
                        kind="O"
                    )
                    created_count += 1

            elif attendance.status != "N":
                # Check if the student already has an "O" (Exit) attendance for the same date
                if not Atendance.objects.filter(
                    student=student,
                    created_at__date=attendance_date,
                    kind="O"
                ).exists():
                    # Create exit attendance
                    Atendance.objects.create(
                        created_at=attendance_date,
                        updated_at=attendance_date,
                        status="O",  # On Time
                        attendance_type="M",  # Manual
                        student=student,
                        created_by="System",
                        observations="Automatically marked as checked out",
                        kind="O"
                    )
                    created_count += 1
            
            

        self.stdout.write(self.style.SUCCESS(f'{created_count} exit attendances created for {attendance_date}.'))
