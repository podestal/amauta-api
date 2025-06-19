from django.core.management.base import BaseCommand
from school.models import Category, School, Instructor
from school.utils import DEFAULT_CATEGORIES

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
        
        instructors = Instructor.objects.filter(school=school)
        if not instructors.exists():
            self.stdout.write(self.style.ERROR(f'No instructors found for school with ID {school_id}.'))
            return
        

        for instructor in instructors:
            if Category.objects.filter(instructor=instructor).exists():
                self.stdout.write(self.style.WARNING(
                    f'Categories already exist for instructor: {instructor.first_name} {instructor.last_name}'
                ))
                continue
            self.stdout.write(self.style.SUCCESS(
                f'Creating categories for instructor: {instructor.first_name} {instructor.last_name}'
            ))
            # Create Categories for the Instructor
            for category_data in DEFAULT_CATEGORIES:
                Category.objects.create(
                    instructor=instructor,
                    title=category_data['title'],
                    weight=category_data['weight']
                )
            self.stdout.write(self.style.SUCCESS(
                f'Created categories for instructor: {instructor.first_name} {instructor.last_name}'
            ))

        self.stdout.write(self.style.SUCCESS(f'\n✅ Done. Categories created for instructors in school: {school.name}'))

