from school import models
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Populate DNIs for student'

    def handle(self, *args, **kwargs):
        i = 0
        students = models.Student.objects.select_related('clase', 'school').prefetch_related('health_info', 'birth_info', 'emergency_contact', 'tutors', 'averages')
        for student in students:
            if not student.dni:
                student.dni = student.uid
                student.save()
                self.stdout.write(self.style.SUCCESS(f'Student "{student}" updated successfully.'))
                i += 1
                
        self.stdout.write(self.style.SUCCESS(f'{i} students updated successfully.'))
