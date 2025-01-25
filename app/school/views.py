from datetime import date
from django.shortcuts import get_object_or_404
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

class SchoolViewSet(ModelViewSet):
    queryset = models.School.objects.all()
    serializer_class = serializers.SchoolSerializer

class CompetenceViewSet(ModelViewSet):
    queryset = models.Competence.objects.all()
    serializer_class = serializers.CompetenceSerializer

class CapacityViewSet(ModelViewSet):
    queryset = models.Capacity.objects.all()
    serializer_class = serializers.CapacitySerializer

class ClaseViewSet(ModelViewSet):
    queryset = models.Clase.objects.prefetch_related('students')
    permission_classes = [IsAdminUser]
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateClaseSerializer
        return serializers.GetClaseSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdminUser()]

class InstructorViewSet(ModelViewSet):

    queryset = models.Instructor.objects.select_related('user').prefetch_related('clases')
    
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
    
class AtendanceViewSet(ModelViewSet):

    queryset = models.Atendance.objects.select_related('student')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateAtendanceSerializer
        return serializers.GetAtendanceSerializer
    
    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAdminUser()]
        return [IsAuthenticated()]

    @action(detail=False, methods=['get'])
    def byClassroom(self, request):
        classroom = request.query_params.get('classroom')
        if not classroom:
            return Response({"error": "Classroom parameter is required"}, status=400)
        attendances = self.queryset.filter(student__clase=classroom, created_at__date=date.today())
        serializer = serializers.GetSimpleAttendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byStudent(self, request):
        student_id = request.query_params.get('student')
        month = request.query_params.get('month')
        print('month', month)
        if not month:
            month = datetime.today().month
        student = get_object_or_404(models.Student, uid=student_id)
        attendances = self.queryset.filter(student=student, created_at__month=month).order_by('-created_at')
        print(f'{student.first_name} attendances', attendances)
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

    queryset = models.Assistant.objects.select_related('user').prefetch_related('clases')
    serializer_class = serializers.GetAssistantSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
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

        filter_range = self.request.query_params.get('range', 'day')

        if filter_range == 'day':
            start_date = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif filter_range == 'week':
            start_date = now - timedelta(days=now.weekday())
        elif filter_range == 'month':
            start_date = now.replace(day=1)
        elif filter_range == 'year':
            start_date = now.replace(month=1, day=1)

        attendance_in = models.Atendance.objects.filter(
            kind='I', created_at__gte=start_date, created_at__lte=now
        )
        attendance_out = models.Atendance.objects.filter(
            kind='O', created_at__gte=start_date, created_at__lte=now
        )

        return (
            models.Student.objects.select_related('clase')
            .prefetch_related(
                Prefetch('atendances', queryset=attendance_in, to_attr='attendance_in'),
                Prefetch('atendances', queryset=attendance_out, to_attr='attendance_out')
            )
        )

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateStudentSerializer
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
            return Response({"error": "No students found"}, status=400)

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


class TutorViewSet(ModelViewSet):
    queryset = models.Tutor.objects.select_related('user').prefetch_related('students')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateTutorSerializer
        return serializers.GetTutorSerializer
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS or self.request.method in ['PUT', 'PATCH']:
            return [IsAuthenticated()]
        return [IsAdminUser()]
    
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
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer  

class AssignatureViewSet(ModelViewSet):
    queryset = models.Assignature.objects.all()
    serializer_class = serializers.AssignatureSerializer  

class ActivityViewSet(ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer  


class GradeViewSet(ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer  

class QuarterGradeViewSet(ModelViewSet):
    queryset = models.QuarterGrade.objects.all()
    serializer_class = serializers.QuarterGradeSerializer  

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

