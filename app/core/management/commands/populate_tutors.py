import random
from django.core.management.base import BaseCommand
from faker import Faker
from school.models import Tutor, Student

fake = Faker()

class Command(BaseCommand):
    help = "Create tutors (Mother and Father) for each student"

    def handle(self, *args, **kwargs):
        students = Student.objects.all()

        if not students.exists():
            self.stdout.write(self.style.WARNING("No students found."))
            return

        tutors_created = 0

        for student in students:
            # Create Mother Tutor
            mother = Tutor.objects.create(
                first_name=fake.first_name_female(),
                last_name=student.last_name,
                phone_number=fake.phone_number(),
                email=fake.email(),
                tutor_type=Tutor.TUTOR_MOTHER,
                civil_status=random.choice([status[0] for status in Tutor.CIVIL_STATUS_CHOICES]),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=50),
                ocupation=fake.job(),
                employer=fake.company(),
                lives_with_student=random.choice([True, False]),
            )
            mother.students.set([student])
            tutors_created += 1

            # Create Father Tutor
            father = Tutor.objects.create(
                first_name=fake.first_name_male(),
                last_name=student.last_name,
                phone_number=fake.phone_number(),
                email=fake.email(),
                tutor_type=Tutor.TUTOR_FATHER,
                civil_status=random.choice([status[0] for status in Tutor.CIVIL_STATUS_CHOICES]),
                address=fake.address(),
                date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=50),
                ocupation=fake.job(),
                employer=fake.company(),
                lives_with_student=random.choice([True, False]),
            )
            father.students.set([student])
            tutors_created += 1

            # Randomly decide whether to create "Other" tutor
            if random.choice([True, False, False]):  # 1/3 chance
                other = Tutor.objects.create(
                    first_name=fake.first_name(),
                    last_name=student.last_name,
                    phone_number=fake.phone_number(),
                    email=fake.email(),
                    tutor_type=Tutor.TUTOR_OTHER,
                    tutor_relationship=fake.random_element(elements=["Uncle", "Guardian", "Sibling"]),
                    civil_status=random.choice([status[0] for status in Tutor.CIVIL_STATUS_CHOICES]),
                    address=fake.address(),
                    date_of_birth=fake.date_of_birth(minimum_age=30, maximum_age=50),
                    ocupation=fake.job(),
                    employer=fake.company(),
                    lives_with_student=random.choice([True, False]),
                )
                other.students.set([student])
                tutors_created += 1

        self.stdout.write(self.style.SUCCESS(f"Successfully created {tutors_created} tutors."))
