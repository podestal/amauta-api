from datetime import date
from rest_framework import serializers
from django.core.cache import cache
from . import models
from django.db.models import Q
from . import utils


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = ['id', 'name', 'type_of_institution', 'picture_name', 'address', 'phone_number', 'email', 'payment_status', 'automatic_late', 'automatic_late_initial']

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
    missing_dni = serializers.SerializerMethodField()

    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section', 'school', 'total_students', 'missing_dni']
    
    def get_total_students(self, obj):
        return obj.students.count()
    
    def get_missing_dni(self, obj):
        return obj.students.filter(dni__isnull=True).count()

class RemoveClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = ['id']
    

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
        fields = ['id', 'user', 'clases_details', 'first_name', 'last_name', 'school', 'phone_number', 'email'] 

    def get_clases_details(self, obj):
        return [
            f"{clase.grade}-{clase.section}-{clase.level}-{clase.id}"
            for clase in obj.clases.all()
        ]

class CreateInstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Instructor
        fields = ['id', 'user', 'clases', 'school', 'phone_number', 'email']

class UpdateInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ['id', 'clases', 'school', 'phone_number', 'email']

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

class CreateAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assistant
        fields = ['id', 'user', 'phone_number', 'email', 'school', 'clases']

class UpdateAssistantSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Assistant
        fields = ['id', 'phone_number', 'email', 'school', 'clases']
    
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
        fields = ['first_name', 'last_name', 'uid', 'dni', 'clase', 'tutor_phone', 'health_info', 'birth_info', 'emergency_contact', 'school', 'is_active']

class GetStudentByAgendaSerializer(serializers.ModelSerializer):

    filtered_read_agendas = serializers.SerializerMethodField()
    filtered_tutor_contact = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['uid', 'first_name', 'last_name', 'tutor_phone', 'filtered_read_agendas', 'filtered_tutor_contact']

    def get_filtered_read_agendas(self, obj):

        if not (hasattr(obj, 'filtered_read_agendas')):
             return False
        return len(obj.filtered_read_agendas) > 0
    
    def get_filtered_tutor_contact(self, obj):

        if not (hasattr(obj, 'filtered_tutor_contact')):
             return False
        return len(obj.filtered_tutor_contact) > 0

    
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
            'tutor_phone',
            'dni',   
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
        return models.Atendance.objects.filter(student=obj.uid).values('status', 'created_at', 'observations', 'kind')

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = [
            'first_name', 
            'last_name', 
            'uid', 
            'clase',
            'prev_school',
            'tutor_phone',
            'dni',
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
            'tutor_phone',
            'dni',
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

class QuarterGradeForStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuarterGrade
        fields = ['id', 'calification', 'competence', 'conclusion']

    

class GetStudentForFilteredGradesSerializer(serializers.ModelSerializer):

    filtered_grades = serializers.SerializerMethodField()
    averages = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['uid', 'first_name', 'last_name', 'filtered_grades', 'averages']

    def get_filtered_grades(self, obj):
        if hasattr(obj, 'filtered_grades'):
            return [
                {
                    'id': grade.id,
                    'calification': grade.calification,
                    'observations': grade.observations if grade.observations else '',
                    'activity': grade.activity.id,
                    'category': grade.activity.category.id,
                    'weight': grade.activity.category.weight,
                }
                for grade in obj.filtered_grades
            ]
        return []
    
    def get_averages(self, obj):
        competence = self.context.get('competence', None)
        if competence:
            return QuarterGradeForStudentSerializer(obj.filtered_averages, many=True).data if hasattr(obj, 'filtered_averages') else []
        else:
            return AssignatureGradeSerializer(obj.filtered_averages, many=True).data if hasattr(obj, 'filtered_averages') else []

class GetStudentForAreaGradeSerializer(serializers.ModelSerializer):
    area_grades = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['uid', 'first_name', 'last_name', 'area_grades']

    def get_area_grades(self, obj):
        if hasattr(obj, 'filtered_area_grades'):
            return [
                {
                    'id': area_grade.id,
                    'calification': area_grade.calification,
                    'area': area_grade.area.id,
                }
                for area_grade in obj.filtered_area_grades
            ]
        return []

class GetStudentForAssignatureGradeSerializer(serializers.ModelSerializer):
    assignature_grades = serializers.SerializerMethodField()
    area_grades = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['uid', 'first_name', 'last_name', 'assignature_grades', 'area_grades']

    def get_assignature_grades(self, obj):
        if hasattr(obj, 'filtered_assignature_grades'):
            return [
                {
                    'id': assignature_grade.id,
                    'calification': assignature_grade.calification,
                    'assignature': assignature_grade.assignature.id,
                }
                for assignature_grade in obj.filtered_assignature_grades
            ]
        return []
    
    def get_area_grades(self, obj):
        if hasattr(obj, 'filtered_area_grade'):
            return [
                {
                    'id': area_grade.id,
                    'calification': area_grade.calification,
                    'area': area_grade.area.id,
                }
                for area_grade in obj.filtered_area_grade
            ]
        return []

class GetStudentForQuarterGradeSerializer(serializers.ModelSerializer):

    averages = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['uid', 'first_name', 'last_name', 'averages']

    def get_averages(self, obj):
        return QuarterGradeForStudentSerializer(obj.filtered_averages, many=True).data if hasattr(obj, 'filtered_averages') else []

class GetStudentForTotalScoreSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()
    average_numeric = serializers.SerializerMethodField()
    average_alphabetical = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['uid', 'first_name', 'last_name', 'total_score', 'average_numeric', 'average_alphabetical']

    def get_total_score(self, obj):
        if not hasattr(obj, 'filtered_averages') or len(obj.filtered_averages) == 0:
            return 0

        total = sum(
            utils.get_from_alphabetical_to_numeric(avg.calification) 
            for avg in obj.filtered_averages 
            if avg.calification is not None
        )

        return total
    
    def get_average_numeric(self, obj):
        if not hasattr(obj, 'filtered_averages') or len(obj.filtered_averages) == 0:
            return 0

        total = self.get_total_score(obj)
        average = total / len(obj.filtered_averages)
        return round(average, 0) if average else 0
    
    def get_average_alphabetical(self, obj):
        if not hasattr(obj, 'filtered_averages') or len(obj.filtered_averages) == 0:
            return 'NA'
        return utils.get_from_numeric_to_alphabetical(self.get_average_numeric(obj))


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
# export interface Assignature {
#     id: number
#     title: string
#     clase: number
#     instructor: number
#     area: number,
# }

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = '__all__'

class AssignatureSerializer(serializers.ModelSerializer):

    classroom_description = serializers.SerializerMethodField()

    class Meta:
        model = models.Assignature
        fields = ['id', 'title', 'clase', 'instructor', 'area', 'classroom_description']

    def get_classroom_description(self, obj):
        return f"{obj.clase.grade}-{obj.clase.section}-{obj.clase.level}"

    

class ActivitySerializer(serializers.ModelSerializer):

    category_name = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = ['id', 'title', 'description', 'due_date', 'category', 'category_name', 'assignature', 'quarter', 'competences', 'capacities', 'lessons']

    def get_category_name(self, obj):
        return obj.category.title


class CreateActivitySerializer(serializers.ModelSerializer):
    category_name = serializers.SerializerMethodField()
    class Meta:
        model = models.Activity
        fields = ['id', 'title', 'description', 'due_date', 'category', 'category_name', 'assignature', 'quarter', 'lessons']
    def get_category_name(self, obj):
        return obj.category.title

class GetActivityForTutorSerializer(serializers.ModelSerializer):

    grade = serializers.SerializerMethodField()
    observations = serializers.SerializerMethodField()

    class Meta:
        model = models.Activity
        fields = ['id', 'title', 'description', 'due_date', 'category', 'grade', 'observations', 'lessons']

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

class GradesByStudentSerializer(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField()
    assignature = serializers.SerializerMethodField()
    due_date = serializers.SerializerMethodField()

    class Meta:
        model = models.Grade
        fields = ['id', 'activity', 'assignature', 'due_date', 'calification', 'observations']

    def get_activity(self, obj):
        return obj.activity.title if obj.activity else None
    
    def get_assignature(self, obj):
        return obj.activity.assignature.title if obj.activity and obj.activity.assignature else None

    def get_due_date(self, obj):
        return obj.activity.due_date if obj.activity else None

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


class AreaGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AreaGrade
        fields = '__all__'

class AssignatureGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AssignatureGrade
        fields = '__all__'

class GetAnnouncementSerializer(serializers.ModelSerializer):

    author = serializers.SerializerMethodField()

    class Meta:
        model = models.Announcement
        fields = ['id', 'title', 'description', 'created_at', 'students', 'clases', 'author', 'announcement_type', 'visibility_level']

    def get_author(self, obj):
        return f'{obj.created_by.first_name} {obj.created_by.last_name}' if obj.created_by else 'Automático'

class CreateAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ['id', 'title', 'description', 'students', 'created_by', 'school', 'clases', 'assignature', 'announcement_type', 'visibility_level']

class DeveloperSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Developer
        fields = '__all__'

class TutorReadAgendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TutorReadAgenda
        fields = '__all__'

class TutorContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TutorContact
        fields = '__all__'

class WhatsappMessageSerialzer(serializers.ModelSerializer):
    class Meta:
        model = models.WhatsappMessage
        fields = '__all__'

class TutorsAuthInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TutorAuthInfo
        fields = '__all__'

class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Balance
        fields = '__all__'

class GetLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = '__all__'


class CreateLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Lesson
        fields = ['id', 'instructor', 'assignature', 'classroom', 'subject', 'content', 'quarter']