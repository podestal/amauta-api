import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from school.models import Assignature, Student, QuarterGrade, Competence

class Command(BaseCommand):
    help = 'Populate quarter grades for a primary class'

    def add_arguments(self, parser):
        parser.add_argument('--classroom', type=int, help='Classroom to create the grades')
        parser.add_argument('--quarter', type=str, help='Quarter to create the grades')

    def handle(self, *args, **kwargs):

        classroomId = kwargs['classroom']
        quarter = kwargs['quarter']
        assignatures = Assignature.objects.filter(clase_id=classroomId).select_related('area', 'clase', 'instructor')

        if not assignatures.exists():
            self.stdout.write(self.style.ERROR('No assignatures found'))
            return
        
        students = Student.objects.filter(clase_id=classroomId).select_related('clase', 'school')
        competences = Competence.objects.select_related('area')

        if not students.exists():
            self.stdout.write(self.style.ERROR('No students found'))
            return
        
        for assignature in assignatures:
            filtered_competences = competences.filter(area=assignature.area)
            for competence in filtered_competences:
                for student in students:
                    calification = random.choice(['AD', 'A', 'B', 'C'])
                    quarter = quarter
                    competence = competence
                    conclusion = ''
                    if calification == 'C':
                        conclusion = 'El estudiante necesita mejorar en esta área.'
                    QuarterGrade.objects.create(
                        calification=calification,
                        student=student,
                        quarter=quarter,
                        assignature=assignature,
                        competence=competence,
                        conclusion=conclusion
                    )
                    self.stdout.write(self.style.SUCCESS(f'Quarter grade for student "{student.first_name} {student.last_name}" in assignature "{assignature.title}" created successfully.'))

        self.stdout.write(self.style.SUCCESS('Quarter grades created successfully.'))
