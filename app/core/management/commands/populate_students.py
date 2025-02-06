from school import models
from faker import Faker
from django.core.management.base import BaseCommand
import random

fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with student data"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Number of students to create')

    def handle(self, *args, **kwargs):
        count = kwargs['count']
        classrooms = models.Clase.objects.all()

        if not classrooms.exists():
            self.stdout.write(self.style.ERROR('No classrooms found'))
            return

        for i in range(count):
            clase = random.choice(classrooms)
            uid = fake.random_int(min=10000000, max=99999999)
            first_name = fake.first_name()
            last_name = fake.last_name()

            student = models.Student.objects.create(
                uid=uid,
                first_name=first_name,
                last_name=last_name,
                clase=clase,
                prev_school=fake.company(),
                main_language=random.choice([lang[0] for lang in models.Student.LANGUAGE_CHOICES]),
                second_language=random.choice([lang[0] for lang in models.Student.LANGUAGE_CHOICES]) if random.choice([True, False]) else None,
                number_of_siblings=random.randint(0, 5),
                place_in_family=random.randint(1, 5),
                religion=random.choice([rel[0] for rel in models.Student.RELIGION_CHOICES]),
                address=fake.address(),
                phone_number=fake.phone_number(),
                celphone_number=fake.phone_number(),
                # map_location=fake.latitude() + ", " + fake.longitude(),
                insurance=random.choice([ins[0] for ins in models.Student.INSURANCE_CHOICES]) if random.choice([True, False]) else None,
                lives_with=fake.name(),
                tutor_name=fake.name(),
            )

            # Create related Health Information
            models.Health_Information.objects.create(
                student=student,
                weight=round(random.uniform(30, 100), 1),
                height=round(random.uniform(1.2, 2.0), 2),
                illness=fake.sentence() if random.choice([True, False]) else None,
            )

            # Create related Birth Info
            models.Birth_Info.objects.create(
                student=student,
                date_of_birth=fake.date_of_birth(minimum_age=6, maximum_age=18),
                state=fake.state(),
                county=fake.city(),
                city=fake.city(),
                natural_birth=random.choice([True, False])
            )

            # Create Emergency Contact
            models.Emergency_Contact.objects.create(
                student=student,
                name=fake.name(),
                phone_number=fake.phone_number(),
                address=fake.address()
            )

            self.stdout.write(self.style.SUCCESS(f'Student {student} created with full data'))

