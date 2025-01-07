from school import models
from faker import Faker
from django.core.management.base import BaseCommand
import random

fake = Faker()

class Command(BaseCommand):
    help = "Populate the database with student data"

    def add_arguments(self, parser):
        parser.add_argument('--count', type=int, default=10, help='Indicates the number of students to be created')

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
            tutor_phone = fake.phone_number()

            student = models.Student.objects.create(
                uid=uid,
                first_name=first_name,
                last_name=last_name,
                clase=clase,
                tutor_phone=tutor_phone
            )

            self.stdout.write(self.style.SUCCESS(f'Student {student} created'))

