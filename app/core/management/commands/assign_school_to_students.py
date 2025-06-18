from django.core.management.base import BaseCommand
from school.models import Student, School

class Command(BaseCommand):
    help = 'Assigns a school to students who have no school set.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--school',
            type=int,
            required=True,
            help='Specify the school ID to assign to students without a school'
        )

    def handle(self, *args, **options):
        school_id = options['school']

        try:
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'School with ID {school_id} does not exist.'))
            return

        students = Student.objects.all()
        updated_count = 0

        for student in students:
            if student.school:
                self.stdout.write(self.style.NOTICE(
                    f'{student.first_name} {student.last_name} (UID: {student.uid}) already assigned to {student.school.name}'
                ))
            else:
                student.school = school
                student.save()
                updated_count += 1
                self.stdout.write(self.style.SUCCESS(
                    f'Assigned school "{school.name}" to {student.first_name} {student.last_name} (UID: {student.uid})'
                ))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done. Total students updated: {updated_count}'))
