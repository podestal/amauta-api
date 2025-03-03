from datetime import date
from unidecode import unidecode
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractDay
from django.utils import timezone
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, IsAuthenticated
from django.db.models import Subquery, OuterRef, Prefetch
from django.core.cache import cache
from datetime import datetime

from notification.push_notifications import send_push_notification
from notification.models import FCMDevice

from . import models
from . import serializers

class AreaViewSet(ModelViewSet):
    queryset = models.Area.objects.all()
    serializer_class = serializers.AreaSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class SchoolViewSet(ModelViewSet):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class CompetenceViewSet(ModelViewSet):
    queryset = models.Competence.objects.select_related('area')
    serializer_class = serializers.CompetenceSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class CapacityViewSet(ModelViewSet):
    queryset = models.Capacity.objects.select_related('competence')
    serializer_class = serializers.CapacitySerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class ClaseViewSet(ModelViewSet):
    queryset = models.Clase.objects.select_related('school').prefetch_related('students')
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateClaseSerializer
        return serializers.GetClaseSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return super().get_queryset()
        school = self.request.query_params.get('school')
        if not school:
            return Response({"error": "School parameter is required"}, status=400)
        return self.queryset.filter(school=school)
    
    # @action(detail=False, methods=['get'])
    # def withStudentsCount(self, request):

    #     school = request.query_params.get('school')
    #     if not school:
    #         return Response({"error": "School parameter is required"}, status=400)
    #     clases = self.queryset.filter(school=school)
    #     serializer = serializers.GetClaseForSummarySerializer(clases, many=True)
    #     return Response(serializer.data)
        

class InstructorViewSet(ModelViewSet):

    queryset = models.Instructor.objects.select_related('user', 'school').prefetch_related('clases')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateInstructorSerializer
        return serializers.GetInstructorSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        user = self.request.user
        try:
            instructor = self.queryset.get(user=user)
        except:
            raise NotFound("Instructor not found for the current user.")
        serializer = serializers.GetInstructorSerializer(instructor)
        return Response(serializer.data)
    
class ManagerViewSet(ModelViewSet):

    queryset = models.Manager.objects.select_related('user', 'school')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateManagerSerializer
        return serializers.GetManagerSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        user = self.request.user
        try:
            manager = self.queryset.get(user=user)
        except:
            raise NotFound("Manager not found for the current user.")
        serializer = serializers.GetManagerSerializer(manager)
        return Response(serializer.data)
    
class AtendanceViewSet(ModelViewSet):

    queryset = models.Atendance.objects.select_related('student')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateAtendanceSerializer
        return serializers.GetAtendanceSerializer
    
    # def get_permissions(self):
    #     if self.request.method == 'DELETE':
    #         return [IsAdminUser()]
    #     return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def byClassroom(self, request):
        '''Get all attendances by classroom and dates'''
        attendances = self.queryset
        classroom = request.query_params.get('classroom')
        week_param = request.query_params.get('week')
        day_param = request.query_params.get('day')
        month_param = request.query_params.get('month')

        if not classroom:
            return Response({"error": "Classroom parameter is required"}, status=400)
        if (week_param):
            attendances = attendances.filter(student__clase=classroom, created_at__week=week_param )
        if (day_param):
            attendances = attendances.filter(student__clase=classroom, created_at__day=day_param, created_at__month=month_param)
        if (month_param):
            attendances = attendances.filter(student__clase=classroom, created_at__month=month_param)
        serializer = serializers.GetSimpleAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byStudent(self, request):
        student_id = request.query_params.get('student')
        if not student_id:
            return Response({"error": "Student parameter is required"}, status=400)
        month = request.query_params.get('month')
        if not month:
            month = datetime.today().month
        student = get_object_or_404(models.Student, uid=student_id)
        attendances = self.queryset.filter(student=student, created_at__month=month).order_by('-created_at')
        if not attendances.exists():
            return Response([])
        serializer = serializers.GetAtendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    def save_to_cache(self, student, kind, status, request, attendance_id=None):

        cache_key = f"attendance_{student.uid}_{kind}"
        cache_data = {
            "id": attendance_id,
            "status": status,
            "kind": kind,
            "created_by": request.data.get('created_by'),
            "observations": request.data.get('observations', ''),
            "created_at": datetime.now().isoformat(),
        }

        cache.set(cache_key, cache_data, timeout=64800)
        print('Cache created', cache_key)
        return cache_data
    
    def get_notification_message(self, student, status):

        message = ''

        if status == 'L':
            message = f'{student.first_name} llegó tarde'
        elif status == 'N':
            message = f'{student.first_name} no asistió'
        elif status == 'T':
            message = f'{student.first_name} se retiró temprano'
        elif status == 'E':
            message = f'{student.first_name} fué excusado'

        return message

    
    def send_notification(self, student, tutor, status, apologize_message=None):

        tokens = FCMDevice.objects.filter(user=tutor.user)
        message = ''
        if apologize_message:
            message = apologize_message
        else:
            message = self.get_notification_message(student, status)

        for token in tokens:
                send_push_notification(token.device_token, 'Alerta de Asistencia', message)

    def update(self, request, *args, **kwargs):
        print('request', request.data)

        status = request.data['status']
        kind = request.data['kind']
        student_id = request.data['student']
        student = models.Student.objects.get(uid=student_id)

        if not student: 
            return Response({"error": "No se pudo encontrar alumno"}, status=400)
        
        try:
            tutor = models.Tutor.objects.get(students=student)
            self.send_notification(student, tutor, status, apologize_message=f'{student.first_name} llegó a tiempo')
        except:
            print('could not find tutor')
        return super().update(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):

        status = request.data['status']
        kind = request.data['kind']
        student_id = request.data['student']
        # attendance_id = ''

        try:
            student = models.Student.objects.get(uid=student_id)
        except:
            return Response({"error": "No se pudo encontrar alumno"}, status=400)

        existing_attendance = models.Atendance.objects.filter(
            student__uid=student_id,
            created_at__date=date.today()
        )

        if existing_attendance.count() == 2:
            return Response({"error": "Alumno ya fué escaneado"}, status=400)
        
        if existing_attendance.count() == 1 and kind == 'I':
            return Response({"error": "Alumno ya fué escaneado"}, status=400)

        if status != 'O':

            try:
                tutor = models.Tutor.objects.get(students=student)
            except:
                # attendance_id = super().create(request, *args, **kwargs).data['id']
                # cache = self.save_to_cache(student, kind, status, request, attendance_id=attendance_id)
                # return Response(cache, status=201)
                return super().create(request, *args, **kwargs)
            
            self.send_notification(student, tutor, status)

            # attendance_id = super().create(request, *args, **kwargs).data['id']

        # cache = self.save_to_cache(student, kind, status, request, attendance_id=attendance_id)
        return super().create(request, *args, **kwargs)
    
class AssistantViewSet(ModelViewSet):

    queryset = models.Assistant.objects.select_related('user', 'school').prefetch_related('clases')
    serializer_class = serializers.GetAssistantSerializer
    
    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS or self.request.method in ['PUT', 'PATCH']:
    #         return [IsAuthenticated()]
    #     return [IsAdminUser()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        user = self.request.user
        try:
            assistant = self.queryset.get(user=user)
        except:
            return Response({"error": "Assistant not found for the current user"}, status=404)
        serializer = serializers.GetAssistantSerializer(assistant)
        return Response(serializer.data)

class StudentViewSet(ModelViewSet):

    def get_queryset(self):

        now = timezone.now()
        current_month = now.month

        day_param = self.request.query_params.get('day')
        week_param = self.request.query_params.get('week')
        month_param = self.request.query_params.get('month', current_month)

        attendance_in = models.Atendance.objects.filter(
            kind='I'
        )
        attendance_out = models.Atendance.objects.filter(
            kind='O'
        )

        if day_param:
            attendance_in = attendance_in.annotate(day=ExtractDay('created_at'), month=ExtractMonth('created_at')).filter(day=int(day_param), month=int(month_param))
            attendance_out = attendance_out.annotate(day=ExtractDay('created_at'), month=ExtractMonth('created_at')).filter(day=int(day_param), month=int(month_param))

        elif week_param:
            attendance_in = attendance_in.annotate(week=ExtractWeek('created_at')).filter(week=int(week_param))
            attendance_out = attendance_out.annotate(week=ExtractWeek('created_at')).filter(week=int(week_param))
        
        elif month_param:
            attendance_in = attendance_in.annotate(month=ExtractMonth('created_at')).filter(month=int(month_param))
            attendance_out = attendance_out.annotate(month=ExtractMonth('created_at')).filter(month=int(month_param))

        else:
            attendance_in = attendance_in.filter(created_at=now.today())
            attendance_out = attendance_out.filter(created_at=now.today())

        return (
                models.Student.objects.select_related('clase', 'school').prefetch_related('health_info', 'birth_info', 'emergency_contact', 'tutors', 'averages')
                .prefetch_related(
                    Prefetch('atendances', queryset=attendance_in, to_attr='attendance_in'),
                    Prefetch('atendances', queryset=attendance_out, to_attr='attendance_out')
                )
            )

    def get_serializer_class(self):

        # if self.action == 'list':
        #     return serializers.GetStudentsSerializer
        if self.request.method == 'POST':
            return serializers.CreateStudentSerializer
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.UpdateStudentSerializer
        return serializers.GetStudentSerializer

    @action(detail=False, methods=['get'])
    def byClassroom(self, request):
        classroom = request.query_params.get('classroom')
        if not classroom:
            return Response({"error": "Classroom parameter is required"}, status=400)
        
        try:
            classroom = int(classroom)
        except ValueError:
            return Response({"error": "Classroom parameter must be an integer"}, status=400)

        students = self.get_queryset().filter(clase=classroom)
        if not students.exists():
            return Response([], status=200)

        serializer = serializers.GetStudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byTutor(self, request):

        user_id = request.user.id
        try: 
            tutor = models.Tutor.objects.get(user_id=user_id)
            students = tutor.students.all()
            serializer = serializers.GetStudentForTutorSerializer(students, many=True)
            return Response(serializer.data)
        except:
            return Response({"error": "Tutor not found"}, status=404)
        
    @action(detail=False, methods=['get'])
    def byName(self, request):
        school = request.query_params.get('school')
        name = request.query_params.get('name')

        if not name:
            return Response({"error": "Name parameter is required"}, status=400)

        normalized_name = unidecode(name)  # Removes accents

        query = (
            Q(first_name__icontains=normalized_name) | 
            Q(last_name__icontains=normalized_name)
        ) & Q(school_id=school)

        students = self.get_queryset().filter(query)
        serializer = serializers.GetStudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byLastTen(self, request):
        school = request.query_params.get('school')
        students = self.get_queryset().filter(school=school).order_by('-created_at')[:10]
        serializer = serializers.GetStudentSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byQuarterGrade(self, request):
        clase = request.query_params.get('clase')
        competencies = request.query_params.get('competencies')
        students = self.get_queryset().filter(clase=clase)
        serializer = serializers.GetStudentForQuarterGradeSerializer(students, many=True, context={'competencies': competencies})
        return Response(serializer.data)
    

class TutorViewSet(ModelViewSet):

    queryset = models.Tutor.objects.select_related('user', 'school').prefetch_related('students')
    permission_classes = [IsAuthenticated]
    
    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return serializers.CreateTutorSerializer
        return serializers.GetTutorSerializer
    
    # def get_permissions(self):
    #     if self.request.method in SAFE_METHODS or self.request.method in ['PUT', 'PATCH']:
    #         return [IsAuthenticated()]
    #     return [IsAdminUser()]
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        user = self.request.user
        try:
            tutor = self.queryset.get(user=user)
        except:
            return Response({"error": "Tutor not found for the current user"}, status=404)
        serializer = serializers.GetTutorSerializer(tutor)
        return Response(serializer.data)

class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.select_related('instructor')
    serializer_class = serializers.CategorySerializer  
    permission_classes = [IsAuthenticated]

    def get_queryset(self):

        if self.request.user.is_superuser:
            return super().get_queryset()
        user = self.request.user
        try:
            instructor = models.Instructor.objects.get(user_id=user.id)
        except:
            return Response({"error": "Instructor not found for the current user"}, status=404)
        return self.queryset.filter(instructor_id=instructor.id)
    
class AssignatureViewSet(ModelViewSet):
    queryset = models.Assignature.objects.select_related('clase', 'instructor', 'area')
    serializer_class = serializers.AssignatureSerializer  

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

    @action(detail=False, methods=['get'])
    def byInstructor(self, request):
        user = self.request.user
        try:
            instructor = models.Instructor.objects.get(user_id=user.id)
        except:
            return Response({"error": "Instructor not found for the current user"}, status=404)
        assignatures = self.queryset.filter(instructor_id=instructor.id)
        serializer = serializers.AssignatureSerializer(assignatures, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byTutor(self, request):
        studentUid = request.query_params.get('student')
        quarter = request.query_params.get('quarter')
        user = self.request.user
        try:
            tutor = models.Tutor.objects.get(user_id=user.id)
        except:
            return Response({"error": "Tutor not found for the current user"}, status=404)
        assignatures = self.queryset.filter(clase__students__tutors=tutor)
        serializer = serializers.GetAssignaturesForTutorSerializer(assignatures, many=True, context={'studentUid': studentUid, 'quarter': quarter})
        return Response(serializer.data)

class ActivityViewSet(ModelViewSet):

    queryset = models.Activity.objects.select_related('assignature', 'category').prefetch_related('competences', 'capacities')
    serializer_class = serializers.ActivitySerializer  
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def byAssignature(self, request):
        assignature = request.query_params.get('assignature')
        if not assignature:
            return Response({"error": "Assignature parameter is required"}, status=400)
        activities = self.queryset.filter(assignature_id=assignature)
        serializer = serializers.ActivitySerializer(activities, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def byTutor(self, request):
        assignature = request.query_params.get('assignature')
        studentUid = request.query_params.get('student')
        quarter = request.query_params.get('quarter')
        if not assignature:
            return Response({"error": "Assignature parameter is required"}, status=400)
        activities = self.queryset.filter(assignature_id=assignature, quarter=quarter)
        serializer = serializers.GetActivityForTutorSerializer(activities, many=True, context={'studentUid': studentUid, 'quarter': quarter})
        return Response(serializer.data)


class GradeViewSet(ModelViewSet):

    queryset = models.Grade.objects.select_related('student', 'activity', 'assignature')
    serializer_class = serializers.GradeSerializer  
    # permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return serializers.GradesByActivitySerializer
        return serializers.GradeSerializer  

    @action(detail=False, methods=['get'])
    def byActivity(self, request):
        activity = request.query_params.get('activity')
        if not activity:
            return Response({"error": "Activity parameter is required"}, status=400)
        grades = self.queryset.filter(activity_id=activity)
        serializer = serializers.GradesByActivitySerializer(grades, many=True)
        return Response(serializer.data)

class QuarterGradeViewSet(ModelViewSet):

    queryset = models.QuarterGrade.objects.select_related('student', 'assignature', 'competence')
    serializer_class = serializers.QuarterGradeSerializer  

    # @action(detail=False, methods=['get'])
    # def forInstructor(self, request):
        # quarter = request.query_params.get('quarter') 
        # assignature = request.query_params.get('assignature')
        # quarter_grades = self.queryset.filter(quarter='Q1', assignature=7)
        # serializer = serializers.GetQuarterGradeForInstructorSerializer(quarter_grades, many=True)
        # return Response(serializer.data)

        # user = self.request.user
        # try:
        #     instructor = models.Instructor.objects.get(user_id=user.id)
        # except:
        #     return Response({"error": "Instructor not found for the current user"}, status=404)
        # quarter_grades = self.queryset.filter(assignature__instructor=instructor)
        # serializer = serializers.QuarterGradeSerializer(quarter_grades, many=True)
        # return Response(serializer.data)

class AnnouncementViewSet(ModelViewSet):

    queryset = models.Announcement.objects.select_related('student').order_by('created_at')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateAnnouncementSerializer
        return serializers.GetAnnouncementSerializer
    
    @action(detail=False, methods=['get'])
    def byStudent(self, request):
        student = request.query_params.get('student')
        if not student:
            return Response({"error": "Student parameter is required"}, status=400)
        announcements = self.queryset.filter(student=student).order_by('-created_at')
        serializer = serializers.GetAnnouncementSerializer(announcements, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byTutor(self, request):
        user_id = request.user.id
        try:    
            tutor = models.Tutor.objects.get(user_id=user_id)
            students = tutor.students.all()
            announcements = models.Announcement.objects.filter(student__in=students).order_by('-created_at')
            if not announcements.exists():
                return Response([], status=200)
            serializer = serializers.GetAnnouncementSerializer(announcements, many=True)
            return Response(serializer.data)

        except models.Tutor.DoesNotExist:
            return Response({"error": "Tutor not found"}, status=404)
        except Exception as e:
            return Response({"error": str(e)}, status=500)
        
    def create(self, request, *args, **kwargs):

        student_id = request.data['student']
        student = models.Student.objects.get(uid=student_id)

        try:
            tutor = models.Tutor.objects.get(students=student)
        except:
            return super().create(request, *args, **kwargs)

        tokens = FCMDevice.objects.filter(user=tutor.user)
        message = f'Tienes un nuevo mensaje sobre {student.first_name}'
        for token in tokens:
                send_push_notification(token.device_token, 'Nuevo Mensaje', message)
        return super().create(request, *args, **kwargs)

class HealthInfoViewSet(ModelViewSet):
    queryset = models.Health_Information.objects.select_related('student')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateHealthInfoSerializer
        return serializers.GetHealthInfoSerializer
    
class BirthInfoViewSet(ModelViewSet):
    queryset = models.Birth_Info.objects.select_related('student')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateBirthInfoSerializer
        return serializers.GetBirthInfoSerializer
    
class EmergencyContactViewSet(ModelViewSet):
    queryset = models.Emergency_Contact.objects.select_related('student')

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateEmergencyContactSerializer
        return serializers.GetEmergencyContactSerializer