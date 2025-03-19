from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from school.models import Atendance, Student
import datetime

class Command(BaseCommand):
    help = 'Populate missing attendances for a specific date with configurable kind and status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--kind',
            type=str,
            choices=['I', 'O'],
            required=True,
            help='Specify the kind of attendance: "I" for Check-in, "O" for Check-out'
        )
        parser.add_argument(
            '--date',
            type=str,
            help='Specify the date in YYYY-MM-DD format. Defaults to the current date.'
        )

    def handle(self, *args, **options):
        kind = options['kind']

        # Parse the date argument or use today's date

        if options['date']:
            try:
                attendance_date = datetime.datetime.strptime(options['date'], '%Y-%m-%d').date()
            except ValueError:
                self.stdout.write(self.style.ERROR('Invalid date format. Use YYYY-MM-DD.'))
                return
        else:
            attendance_date = timezone.localdate()
        
        self.stdout.write(self.style.SUCCESS(
            f'{attendance_date} Date'
        ))

        missing_attendance_count = 0
        status = "N" if kind == "I" else "O"

        # Filtering students based on missing attendance
        if kind == "O":
            students_without_attendance = Student.objects.filter(
                atendances__created_at__date=attendance_date,
                atendances__kind="I"
            ).exclude(
                atendances__created_at__date=attendance_date,
                atendances__kind="O"
            ).exclude(
                atendances__created_at__date=attendance_date,
                atendances__kind="I",
                atendances__status="N"
            ).distinct()

        else:
            students_without_attendance = Student.objects.exclude(
                atendances__created_at__date=attendance_date,
                atendances__kind="I"
            )
    
        self.stdout.write(self.style.SUCCESS(
            f'Students without attendance: {students_without_attendance.count()}'
        ))

        for student in students_without_attendance:
            Atendance.objects.create(
                created_at=attendance_date,
                updated_at=attendance_date,
                status=status,
                attendance_type="M",  # Morning
                student=student,
                created_by="System",
                observations="Automatically marked as absent" if kind == "I" else "Automatically marked as checked out",
                kind=kind,
            )
            missing_attendance_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{missing_attendance_count} missing attendances created for {attendance_date} with kind "{kind}".'
        ))
