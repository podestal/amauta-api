import csv
from django.core.management.base import BaseCommand
from school import models
from django.utils.text import slugify
from pathlib import Path
import random


grade_converter = {
    'PRIMERO': '1',
    'SEGUNDO': '2',
    'TERCERO': '3',
    'CUARTO': '4',
    'QUINTO': '5',
    'SEXTO': '6',
    '3 AÑOS': '3',
    '4 AÑOS': '4',
    '5 AÑOS': '5',
}

level_converter = {
    1: 'I',
    2: 'P',
    3: 'S',
}

class Command(BaseCommand):
    help = "Import students from a CSV file and populate the database"

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, required=True, help='Path to the CSV file')
        parser.add_argument('--school', type=int, required=True, help='School ID to associate with students')

    def handle(self, *args, **options):
        file_path = Path(options['file'])
        school_id = options['school']

        counter = 0

        if not file_path.exists():
            self.stderr.write(self.style.ERROR(f"File not found: {file_path}"))
            return

        # classrooms = {c.external_id: c for c in models.Clase.objects.filter(school_id=school_id)}

        # created_count = 0
        school = models.School.objects.get(id=school_id)

        if not school:
            self.stderr.write(self.style.ERROR(f"School with ID {school_id} does not exist."))
            return

        print(f"School: {school.name} (ID: {school.id})")

        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                grade = row.get("description")
                level = row.get("level_id")
                print(f"creating class ... Grade {grade_converter.get(grade)} Level {level_converter.get(int(level))}")
                classroom, created  = models.Clase.objects.get_or_create(
                    school=school,
                    grade=grade_converter.get(grade),
                    level=level_converter.get(int(level)),
                )

                print('classroom created:', classroom)
                if not created:
                    print(f"Classroom already exists: {classroom}")

                student, created = models.Student.objects.get_or_create(
                    clase=classroom,
                    first_name=row.get('nombres'),
                    last_name=f"{row.get('apellido_paterno')} {row.get('apellido_materno')}".strip(),
                    dni=row.get('dni'),
                )
                print(f"Student: {student.first_name} {student.last_name} (ID: {student.dni}) Classroom: {classroom.grade} {classroom.level} ")
                counter += 1
                

        print(f"Total records processed: {counter}")
                
