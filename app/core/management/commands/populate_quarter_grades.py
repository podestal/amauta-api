import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from school.models import Atendance, Student

class Command(BaseCommand):
    help = 'Populate quarter grades for a primary class'

    def add_arguments(self, parser):
        parser.add_argument('--classroom', type=int, help='Classroom to create the grades')

    def handle(self, *args, **kwargs):
        classroomId = kwargs['classroom']
