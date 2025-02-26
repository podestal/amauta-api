from django.core.management.base import BaseCommand
from django.utils import timezone
from school.models import Atendance, Student

class Command(BaseCommand):
    help = 'Populate missing attendances for today with status "N", type "M", and kind "I"'

    def handle(self, *args, **options):
        today = timezone.localdate()
        missing_attendance_count = 0

        # Get students who do NOT have an attendance record for today
        students_without_attendance = Student.objects.exclude(
            atendances__created_at__date=today
        )

        for student in students_without_attendance:
            Atendance.objects.create(
                created_at=today,
                updated_at=today,
                status="N",  # Not attended
                attendance_type="M",  # Morning
                student=student,
                created_by="System",
                observations="Automatically marked as absent",
                kind="I",  # Check-in
            )
            missing_attendance_count += 1

        self.stdout.write(self.style.SUCCESS(
            f'{missing_attendance_count} missing attendances created successfully for today.'
        ))
