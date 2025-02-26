from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from school.models import Atendance, Student

class Command(BaseCommand):
    help = 'Populate missing attendances for today with configurable kind and status'

    def add_arguments(self, parser):
        parser.add_argument(
            '--kind',
            type=str,
            choices=['I', 'O'],
            required=True,
            help='Specify the kind of attendance: "I" for Check-in, "O" for Check-out'
        )

    def handle(self, *args, **options):
        today = timezone.localdate()
        missing_attendance_count = 0
        kind = options['kind']

        # Set status based on kind
        status = "N" if kind == "I" else "O"

        # If kind is "O" (Check-out), filter out students who were absent in "I" (Check-in)
        if kind == "O":
            students_without_attendance = Student.objects.exclude(
                atendances__created_at__date=today,
                atendances__kind="O"
            ).exclude(
                Q(atendances__created_at__date=today, atendances__kind="I", atendances__status="N")
            )
        else:
            # For kind "I", simply exclude students who already have an attendance "I" today
            students_without_attendance = Student.objects.exclude(
                atendances__created_at__date=today,
                atendances__kind="I"
            )

        for student in students_without_attendance:
            Atendance.objects.create(
                created_at=today,
                updated_at=today,
                status=status,
                attendance_type="M",  # Morning
                student=student,
                created_by="System",
                observations="Automatically marked as absent" if kind == "I" else "Automatically marked as checked out",
                kind=kind,
            )
            missing_attendance_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{missing_attendance_count} missing attendances created successfully for today with kind "{kind}".'
        ))
