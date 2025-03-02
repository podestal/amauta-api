from datetime import date
from rest_framework import serializers
from django.core.cache import cache
from . import models

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = ['id', 'name', 'type_of_institution', 'picture_name', 'address', 'phone_number', 'email']

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Competence
        fields = '__all__'

class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Capacity
        fields = '__all__'

class GetHealthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Health_Information
        fields = ['id', 'weight', 'height', 'illness', 'handycap', 'hsndyCap_description', 'saanee', 'psicopedagogic']

class CreateHealthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Health_Information
        fields = ['id', 'weight', 'height', 'illness', 'student', 'handycap', 'hsndyCap_description', 'saanee', 'psicopedagogic']

class GetBirthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Birth_Info
        fields = ['id', 'date_of_birth', 'state', 'county', 'city', 'natural_birth']

class CreateBirthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Birth_Info
        fields = ['id', 'date_of_birth', 'state', 'county', 'city', 'natural_birth', 'student']

class GetEmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Emergency_Contact
        fields = ['id', 'name', 'phone_number', 'address']


class CreateEmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Emergency_Contact
        fields = ['id', 'name', 'phone_number', 'address', 'student']


class GetClaseSerializer(serializers.ModelSerializer):

    total_students = serializers.SerializerMethodField()
    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section', 'school', 'total_students']
    
    def get_total_students(self, obj):
        return obj.students.count()
    

class GetSimpleClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section', 'school']

class CreateClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section', 'school']

class GetManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager
        fields = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'email', 'school']

class CreateManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Manager
        fields = ['id', 'user', 'phone_number', 'email', 'school']


class GetInstructorSerializer(serializers.ModelSerializer):

    clases_details = serializers.SerializerMethodField()

    class Meta: 
        model = models.Instructor
        fields = ['id', 'user', 'clases_details', 'first_name', 'last_name', 'school']

    def get_clases_details(self, obj):
        return [
            f"{clase.grade}-{clase.section}-{clase.level}-{clase.id}"
            for clase in obj.clases.all()
        ]

class CreateInstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Instructor
        fields = ['id', 'user', 'clases', 'school']

class GetAtendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'student', 'status', 'created_by', 'created_at', 'updated_at', 'observations', 'attendance_type', 'kind']

class GetSimpleAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'status', 'student', 'attendance_type', 'kind']

class SimpleAtendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'status', 'observations', 'kind', 'created_at']

class CreateAtendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'student', 'status', 'created_by', 'observations', 'attendance_type', 'kind']

class GetAssistantSerializer(serializers.ModelSerializer):

    clases_details = serializers.SerializerMethodField()

    class Meta:
        model = models.Assistant
        fields = ['id', 'user', 'first_name', 'last_name', 'phone_number', 'address', 'email', 'clases_details', 'school']

    def get_clases_details(self, obj):
        return [
            f"{clase.grade}-{clase.section}-{clase.level}-{clase.id}"
            for clase in obj.clases.all()
        ]
    
class GetTutorForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutor
        fields = [
            'id', 
            'first_name', 
            'last_name', 
            'phone_number', 
            'address', 
            'email', 
            'dni',
            'date_of_birth',
            'state',
            'county',
            'city',
            'ocupation',
            'employer',
            'civil_status',
            'lives_with_student',
            'tutor_type',
            'instruction_grade',
            'school',
        ]

class GetStudentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Student
        fields = ['first_name', 'last_name', 'uid', 'clase', 'health_info', 'birth_info', 'emergency_contact', 'school', 'is_active']

    
class GetStudentSerializer(serializers.ModelSerializer):

    health_info = GetHealthInfoSerializer()
    birth_info = GetBirthInfoSerializer()
    clase = GetSimpleClaseSerializer()
    emergency_contact = GetEmergencyContactSerializer()
    attendances_in = serializers.SerializerMethodField()
    attendances_out = serializers.SerializerMethodField()
    tutors = GetTutorForStudentSerializer(many=True)

    class Meta:
        model = models.Student
        fields = [
            'first_name', 
            'last_name', 
            'clase',
            'uid', 
            'attendances_in', 
            'attendances_out', 
            'created_at',
            'prev_school',
            'main_language',
            'second_language',
            'number_of_siblings',
            'place_in_family',
            'religion',
            'address',
            'phone_number',
            'celphone_number',
            'map_location',
            'insurance',
            'other_insurance',
            'lives_with',
            'health_info',
            'birth_info',
            'emergency_contact',
            'tutors',
            'school',
            'is_active',
        ]

    def get_attendances_in(self, obj):
        attendance_in = getattr(obj, 'attendance_in', None)
        try:
            return [SimpleAtendanceSerializer(attendance).data for attendance in attendance_in] if attendance_in else []
        except:
            return []
            
    
    def get_attendances_out(self, obj):
        attendance_out = getattr(obj, 'attendance_out', None)
        try:
            return [SimpleAtendanceSerializer(attendance).data for attendance in attendance_out ]if attendance_out else []
        except:
            return []

    
class GetStudentForTutorSerializer(serializers.ModelSerializer):

    clase = GetSimpleClaseSerializer()
    attendances = serializers.SerializerMethodField()

    class Meta: 
        model = models.Student
        fields = ['first_name', 'last_name', 'uid', 'clase', 'attendances', 'created_at', 'is_active']

    def get_attendances(self, obj):
        return models.Atendance.objects.filter(student=obj.uid).values('status', 'created_at', 'observations')

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'first_name', 
            'last_name', 
            'uid', 
            'clase',
            'prev_school',
            'main_language',
            'second_language',
            'number_of_siblings',
            'place_in_family',
            'religion',
            'address',
            'phone_number',
            'celphone_number',
            'map_location',
            'insurance',
            'other_insurance',
            'lives_with',
            'school',
            'is_active',
        ]

class UpdateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'first_name', 
            'last_name', 
            'clase',
            'uid', 
            'created_at',
            'prev_school',
            'main_language',
            'second_language',
            'number_of_siblings',
            'place_in_family',
            'religion',
            'address',
            'phone_number',
            'celphone_number',
            'map_location',
            'insurance',
            'other_insurance',
            'lives_with',
            'school',
            'is_active',
        ]

class GetTutorSerializer(serializers.ModelSerializer):

    students = GetStudentForTutorSerializer(many=True)

    class Meta:
        model = models.Tutor
        fields = ['id', 'students', 'first_name', 'last_name', 'phone_number', 'address', 'email', 'can_access', 'tutor_type', 'school']

class CreateTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutor
        fields = [
            'id', 
            'user', 
            'students', 
            'phone_number', 
            'address', 
            'email', 
            'dni',
            'date_of_birth',
            'state',
            'county',
            'city',
            'ocupation',
            'instruction_grade',
            'employer',
            'civil_status',
            'lives_with_student',
            'first_name',
            'last_name',
            'tutor_type',
            'tutor_relationship',
            'school',
        ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class AssignatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assignature
        fields = '__all__'

    

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Activity
        fields = '__all__'

class GetActivityForTutorSerializer(serializers.ModelSerializer):

    grade = serializers.SerializerMethodField()
    observations = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = ['id', 'title', 'description', 'due_date', 'category', 'grade', 'observations']

    def get_grade(self, obj):
        studentUid =  self.context['studentUid']
        quarter = self.context['quarter']
        grade = models.Grade.objects.get(activity=obj.id, student_id=studentUid, activity__quarter=quarter)
        return grade.calification if grade.calification else 'NA'
    
    def get_observations(self, obj):
        studentUid =  self.context['studentUid']
        quarter = self.context['quarter']
        grade = models.Grade.objects.get(activity=obj.id, student_id=studentUid, activity__quarter=quarter)
        return grade.observations if grade.observations else ''

class GetAssignaturesForTutorSerializer(serializers.ModelSerializer):

    # grades
    # averages
    # activities = GetActivityForTutorSerializer(many=True)
    average = serializers.SerializerMethodField()

    class Meta:
        model = models.Assignature
        fields = ['id', 'title', 'average']

    def get_average(self, obj):

        gradeConverter = {
            'C': 1,
            'B': 2,
            'A': 3,
            'AD': 4,
            'NA': 1
        }

        gradeConverterReverse = {
            0: 'NA',
            1: 'C',
            2: 'B',
            3: 'A',
            4: 'AD',
        }

        studentUid =  self.context['studentUid']
        quarter = self.context['quarter']
        grades = models.Grade.objects.filter(activity__assignature=obj.id, student_id=studentUid, activity__quarter=quarter).prefetch_related('activity').select_related('student', 'activity', 'assignature')
        numericGrade = sum([gradeConverter[grade.calification] for grade in grades]) / len(grades) if grades else 0
        average = gradeConverterReverse[round(round(numericGrade, 0))]
        return average

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'

class GetStudentForGradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['first_name', 'last_name', 'uid']

class GradesByActivitySerializer(serializers.ModelSerializer):

    student = GetStudentForGradesSerializer()

    class Meta:
        model = models.Grade
        fields = ['id', 'student', 'calification', 'observations']

class QuarterGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuarterGrade
        fields = '__all__'

class GetAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ['id', 'title', 'description', 'created_at', 'student', 'created_by']

class CreateAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ['id', 'title', 'description', 'student', 'created_by']
