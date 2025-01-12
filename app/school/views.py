from datetime import date
from django.shortcuts import render, get_object_or_404
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.db.models import Prefetch
from django.db.models import Subquery, OuterRef, TextField
from datetime import datetime

from notification.push_notifications import send_push_notification
from notification.models import PushSubscription

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
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateClaseSerializer
        return serializers.GetClaseSerializer

class InstructorViewSet(ModelViewSet):
    queryset = models.Instructor.objects.select_related('user').prefetch_related('clases')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateInstructorSerializer
        return serializers.GetInstructorSerializer
    
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
        if not attendances.exists():
            return Response([])
        serializer = serializers.GetAtendanceSerializer(attendances, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):

        if request.data['status'] != 'O':
            student_id = request.data['student']
            print('student_id', student_id)
            student = models.Student.objects.get(uid=student_id)
            print('student', student)
            tutor = models.Tutor.objects.get(students=student)
            print('tutor', tutor)
            subscriptions = PushSubscription.objects.filter(user=tutor.user)
            print('subscriptions', subscriptions)
            for subscription in subscriptions:
                send_push_notification(subscription, 'Attendance Alert', 'Your student was marked absent')
                print('notification sent')

        # return super().create(request, *args, **kwargs)
        return Response({"success": True})

class StudentViewSet(ModelViewSet):
    def get_queryset(self):

        today = date.today()

        today_attendance = models.Atendance.objects.filter(
            student=OuterRef('uid'), 
            created_at__date=today
        ).order_by('id')

        return (
            models.Student.objects.select_related('clase')
            .annotate(
                today_attendance=Subquery(
                    today_attendance.values('id')[:1]
                )
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

    queryset = models.Announcement.objects.select_related('student')
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.CreateAnnouncementSerializer
        return serializers.GetAnnouncementSerializer
    
    @action(detail=False, methods=['get'])
    def byStudent(self, request):
        student = request.query_params.get('student')
        if not student:
            return Response({"error": "Student parameter is required"}, status=400)
        announcements = self.queryset.filter(student=student)
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
        tutor = models.Tutor.objects.get(students=student)
        subscription = PushSubscription.objects.get(user=tutor.user)

        send_push_notification(subscription, 'New Announcement', 'You have a new announcement')
        return super().create(request, *args, **kwargs)

