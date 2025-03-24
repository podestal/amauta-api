from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db import transaction

import random

class Area(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class School(models.Model):

    name = models.CharField(max_length=255)
    type_of_institution = models.CharField(max_length=255, null=True, blank=True)
    picture_name = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    
    def __str__(self):
        return self.name

    
class Competence(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Capacity(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Clase(models.Model):

    GRADE_FIRST = '1'
    GRADE_SECOND = '2'
    GRADE_THIRD = '3'
    GRADE_FOURTH = '4'
    GRADE_FIFTH = '5'
    GRADE_SIXTH = '6'

    GRADE_CHOICES = [
        (GRADE_FIRST, 'First'),
        (GRADE_SECOND, 'Second'),
        (GRADE_THIRD, 'Third'),
        (GRADE_FOURTH, 'Fourth'),
        (GRADE_FIFTH, 'Fifth'),
        (GRADE_SIXTH, 'Sixth'),
    ]

    LELEL_INITIAL = 'I'
    LEVEL_PRIMARY = 'P'
    LEVEL_SECONDARY = 'S'

    LEVEL_CHOICES = [
        (LEVEL_PRIMARY, 'Primary'),
        (LEVEL_SECONDARY, 'Secondary'),
        (LELEL_INITIAL, 'Initial'),
    ]

    school = models.ForeignKey(School, on_delete=models.CASCADE, null=True, blank=True)
    grade =  models.CharField(max_length=1, choices=GRADE_CHOICES, null=True, blank=True)
    level = models.CharField(max_length=1, choices=LEVEL_CHOICES)
    section = models.CharField(max_length=1, default='U')

    def __str__(self):
        return f'{self.grade}-{self.section}-{self.level}'
    
class Instructor(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='instructor')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='instructors', null=True, blank=True)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    clases = models.ManyToManyField(Clase, related_name='instructors')
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)

class Student(models.Model):

    SPANISH_LANGUAGE = 'S'
    ENGLISH_LANGUAGE = 'E'
    QUECHUA_LANGUAGE = 'Q'
    AYMARA_LANGUAGE = 'A'

    LANGUAGE_CHOICES = [
        (SPANISH_LANGUAGE, 'Spanish'),
        (ENGLISH_LANGUAGE, 'English'),
        (QUECHUA_LANGUAGE, 'Quechua'),
        (AYMARA_LANGUAGE, 'Aymara'),
    ]

    CATHOLIC_RELIGION = 'C'
    EVANGELIC_RELIGION = 'E'
    JEWISH_RELIGION = 'J'
    MUSLIM_RELIGION = 'I'
    BUDDHIST_RELIGION = 'B'
    MORMON_RELIGION = 'M'
    JEHOVAH_RELIGION = 'T'
    CHRISTIAN_RELIGION = 'R'
    OTHER_RELIGION = 'O'

    RELIGION_CHOICES = [
        (CATHOLIC_RELIGION, 'Catholic'),
        (EVANGELIC_RELIGION, 'Evangelic'),
        (JEWISH_RELIGION, 'Jewish'),
        (MUSLIM_RELIGION, 'Muslim'),
        (BUDDHIST_RELIGION, 'Buddhist'),
        (MORMON_RELIGION, 'Mormon'),
        (JEHOVAH_RELIGION, 'Jehovah'),
        (CHRISTIAN_RELIGION, 'Christian'),
        (OTHER_RELIGION, 'Other'),
    ]

    ESSALUD_INSURANCE = 'E'
    PRIVATE_INSURANCE = 'P'
    SIS_INSURANCE = 'S'
    OTHER_INSURANCE = 'O'
    # NOT_SPECIFIED_INSURANCE = 'N'

    INSURANCE_CHOICES = [
        (ESSALUD_INSURANCE, 'Essalud'),
        (PRIVATE_INSURANCE, 'Private'),
        (SIS_INSURANCE, 'SIS'),
        (OTHER_INSURANCE, 'Other'),

    ]

    def generate_uid():
        """Generate a unique 8-digit UID."""
        while True:
            uid = random.randint(10_000_000, 99_999_999)
            if not Student.objects.filter(uid=uid).exists():
                return uid

    uid = models.BigIntegerField(primary_key=True, unique=True, default=generate_uid, editable=False)
    dni = models.CharField(max_length=8, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    clase = models.ForeignKey(Clase, on_delete=models.PROTECT, related_name='students')
    tutor_phone = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='students', null=True, blank=True)
    prev_school = models.CharField(max_length=255, null=True, blank=True)
    main_language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES, default=SPANISH_LANGUAGE)
    second_language = models.CharField(max_length=1, choices=LANGUAGE_CHOICES, null=True, blank=True)
    number_of_siblings = models.IntegerField(default=0)
    place_in_family = models.IntegerField(default=0)
    religion = models.CharField(max_length=1, choices=RELIGION_CHOICES, default=CATHOLIC_RELIGION)
    address = models.TextField(blank=True, null=True)
    phone_number = models.CharField(max_length=255, blank=True, null=True)
    celphone_number = models.CharField(max_length=255, blank=True, null=True)
    map_location = models.CharField(max_length=255, blank=True, null=True)
    insurance = models.CharField(max_length=1, choices=INSURANCE_CHOICES, blank=True, null=True)
    other_insurance= models.CharField(max_length=255, blank=True, null=True)
    lives_with = models.CharField(max_length=255, blank=True, null=True)
    tutor_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Health_Information(models.Model):

    HANDYCAP_CHOICES = [
        ('V', 'Visual'),
        ('A', 'Autism'),
        ('M', 'Motor'),
        ('C', 'Cognitive'),
        ('P', 'Psychological'),
        ('H', 'Hearing-Vision'),
        ('O', 'Other'),
        ('N', 'None'),
    ]

    weight = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    illness = models.TextField(null=True, blank=True)
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='health_info')
    handycap = models.CharField(max_length=1, choices=HANDYCAP_CHOICES, default='N')
    hsndyCap_description = models.TextField(null=True, blank=True)
    saanee = models.BooleanField(default=False)
    psicopedagogic = models.BooleanField(default=False)
    
class Birth_Info(models.Model):

    date_of_birth = models.DateField()
    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='birth_info')
    state = models.CharField(max_length=255)
    county = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    natural_birth = models.BooleanField(default=True)
    
class Emergency_Contact(models.Model):

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name="emergency_contact")
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    address = models.TextField()
    
class Assistant(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    clases = models.ManyToManyField(Clase, related_name='assistants')
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='assistants', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)
    
class Atendance(models.Model):

    STATUS_CHOICES = [
        ('O', 'On Time'),
        ('L', 'Late'),
        ('N', 'Not Attended'),
        ('E', 'Excused'),
        ('T', 'Left Early'),
    ]

    TYPE_CHOICES = [
        ('A', 'Automatic'), 
        ('M', 'Manual')
    ]

    KIND_CHOICES = [
        ('I', 'Entrance'),
        ('O', 'Exit'),
    ]

    created_at = models.DateTimeField(default=timezone.now, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    attendance_type = models.CharField(max_length=1, choices=TYPE_CHOICES)
    kind = models.CharField(max_length=1, choices=KIND_CHOICES, default='I')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, to_field='uid', related_name='atendances')
    created_by = models.CharField(max_length=255)
    observations = models.TextField(null=True, blank=True)

class Developer(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)

class Manager(models.Model):
    
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='managers', null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self, *args, **kwargs):
        if self.user:
            self.first_name = self.user.first_name
            self.last_name = self.user.last_name
        super().save(*args, **kwargs)

class Tutor(models.Model):

    TUTOR_MOTHER = 'M'
    TUTOR_FATHER = 'F'
    TUTOR_OTHER = 'O'

    TUTOR_TYPE_CHOICES = [
        (TUTOR_MOTHER, 'Mother'),
        (TUTOR_FATHER, 'Father'),
        (TUTOR_OTHER, 'Other'),
    ]

    CIVIL_STATUS_SINGLE = 'S'
    CIVIL_STATUS_MARRIED = 'M'
    CIVIL_STATUS_DIVORCED = 'D'
    CIVIL_STATUS_WIDOWED = 'W'
    CIVIL_STATUS_OTHER = 'O'

    CIVIL_STATUS_CHOICES = [
        (CIVIL_STATUS_SINGLE, 'Single'),
        (CIVIL_STATUS_MARRIED, 'Married'),
        (CIVIL_STATUS_DIVORCED, 'Divorced'),
        (CIVIL_STATUS_WIDOWED, 'Widowed'),
        (CIVIL_STATUS_OTHER, 'Other'),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    students = models.ManyToManyField(Student, related_name='tutors')
    dni = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    state = models.CharField(max_length=255, null=True, blank=True)
    county = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    instruction_grade = models.CharField(max_length=255, null=True, blank=True)
    ocupation = models.CharField(max_length=255, null=True, blank=True)
    employer = models.CharField(max_length=255, null=True, blank=True)
    civil_status = models.CharField(max_length=1, choices=CIVIL_STATUS_CHOICES, null=True, blank=True)
    lives_with_student = models.BooleanField(blank=True, null=True) 
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    can_access = models.BooleanField(default=True)
    tutor_type = models.CharField(max_length=1, choices=TUTOR_TYPE_CHOICES, default=TUTOR_MOTHER)
    tutor_relationship = models.CharField(max_length=255, null=True, blank=True)
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name='tutors', null=True, blank=True)


    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    
class Category(models.Model):

    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='categories')
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    weight = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.title} '
    
class Assignature(models.Model):

    title = models.CharField(max_length=255)
    clase =  models.ForeignKey(Clase, on_delete=models.CASCADE, related_name='assignatures')
    instructor = models.ForeignKey(Instructor, on_delete=models.SET_NULL, blank=True, null=True, related_name='assignatures')
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Activity(models.Model):

    QUARTER_CHOICES = [
        ('Q1', 'First Quarter'),
        ('Q2', 'Second Quarter'),
        ('Q3', 'Third Quarter'),
        ('Q4', 'Fourth Quarter'),
    ]

    title = models.CharField(max_length=255)
    assignature = models.ForeignKey(Assignature, on_delete=models.CASCADE, related_name='activities')
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True)
    quarter = models.CharField(max_length=2, choices=QUARTER_CHOICES)
    competences =  models.ManyToManyField(Competence, related_name='activities')
    capacities = models.ManyToManyField(Capacity, related_name='activities')

    def save(self, *args, **kwargs):
        is_new = self.pk is None  # Check if this is a new activity being created
        super().save(*args, **kwargs)  # Save the activity first

        if is_new:  # Only create grades for a new activity
            clase = self.assignature.clase
            students = Student.objects.filter(clase=clase)
            
            grades = [
                Grade(student=student, activity=self, assignature=self.assignature)
                for student in students
            ]
            
            if grades:
                with transaction.atomic():  # Ensure atomicity
                    Grade.objects.bulk_create(grades)


    def __str__(self):
        return self.title
    

class Grade(models.Model):

    CALIFICATION_CHOICES = [
        ('NA', 'NA'),
        ('AD', 'AD'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    ]

    calification = models.CharField(max_length=2, choices=CALIFICATION_CHOICES, default='NA')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='grades')
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, related_name='grades')
    assignature = models.ForeignKey(Assignature, on_delete=models.CASCADE, related_name='grades')
    created_at = models.DateField(auto_now_add=True)
    observations = models.TextField(null=True, blank=True)

class QuarterGrade(models.Model):

    CALIFICATION_CHOICES = [
        ('AD', 'AD'),
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C')
    ]

    QUARTER_CHOICES = [
        ('Q1', 'First Quarter'),
        ('Q2', 'Second Quarter'),
        ('Q3', 'Third Quarter'),
        ('Q4', 'Fourth Quarter'),
    ]

    calification = models.CharField(max_length=2, choices=CALIFICATION_CHOICES)
    assignature = models.ForeignKey(Assignature, on_delete=models.CASCADE, related_name='averages')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='averages')
    quarter = models.CharField(max_length=2, choices=QUARTER_CHOICES)
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='averages')
    conclusion = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            exist = QuarterGrade.objects.filter(
                student=self.student,
                assignature=self.assignature,
                quarter=self.quarter,
                competence=self.competence
            ).exists()

            if exist:
                raise ValueError('This quarter grade already exists')

        
        super().save(*args, **kwargs)

class Announcement(models.Model):

    ANNOUNCEMENT_TYPES = [
        ("I", "Informative"),
        ("A", "Attention"),
        ("E", "Emergency"),
    ]

    VISIBILITY_LEVELS = [
        ("G", "General"),    
        ("C", "Clase"),    
        ("A", "Assignature"),     
        ("P", "Personal"),     
    ]   

    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    announcement_type = models.CharField(max_length=1, choices=ANNOUNCEMENT_TYPES, default='I')
    visibility_level = models.CharField(max_length=1, choices=VISIBILITY_LEVELS, default='G')

    # Relationships
    school = models.ForeignKey(School, on_delete=models.CASCADE, related_name="announcements")
    clases = models.ManyToManyField(Clase, blank=True, related_name="announcements") 
    assignature = models.ForeignKey(Assignature, on_delete=models.CASCADE, null=True, blank=True, related_name="announcements")  
    students = models.ManyToManyField(Student, blank=True, related_name="announcements") 
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.get_visibility_level_display()} - {self.title}"
    
class TutorReadAgenda(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='read_agendas')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='read_agendas')
    read_at = models.DateTimeField(auto_now_add=True)
