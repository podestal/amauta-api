from school import models
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Update existing students to assign them to school ID 1"

    def handle(self, *args, **kwargs):
        school = models.School.objects.filter(id=1).first()  # Get School with ID 1

        if not school:
            self.stdout.write(self.style.ERROR('School with ID 1 not found'))
            return

        students_to_update = models.Student.objects.filter(school__isnull=True)  # Find students without a school

        if not students_to_update.exists():
            self.stdout.write(self.style.SUCCESS('No students needed updating.'))
            return

        updated_count = students_to_update.update(school=school)  # Bulk update all students

        self.stdout.write(self.style.SUCCESS(f'Successfully updated {updated_count} students to be assigned to {school.name}'))
