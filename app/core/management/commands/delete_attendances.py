from django.core.management.base import BaseCommand
from school.models import Atendance

class Command(BaseCommand):
    help = 'Delete all attendances from the database'

    def handle(self, *args, **options):
        attendance_count = Atendance.objects.count()

        if attendance_count == 0:
            self.stdout.write(self.style.WARNING('No attendances found to delete.'))
            return

        # Delete all attendance records
        Atendance.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {attendance_count} attendances.'))
