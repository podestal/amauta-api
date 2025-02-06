from school import models
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Delete all students and their related data"

    def handle(self, *args, **kwargs):
        students_count = models.Student.objects.count()

        if students_count == 0:
            self.stdout.write(self.style.WARNING('No students found to delete.'))
            return

        models.Health_Information.objects.all().delete()
        models.Birth_Info.objects.all().delete()
        models.Emergency_Contact.objects.all().delete()
        
        # Delete all students
        models.Student.objects.all().delete()

        self.stdout.write(self.style.SUCCESS(f'Successfully deleted {students_count} students and their related data.'))
