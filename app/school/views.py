from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

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
    queryset = models.Clase.objects.all()
    serializer_class = serializers.ClaseSerializer

class InstructorViewSet(ModelViewSet):
    queryset = models.Instructor.objects.all()
    serializer_class = serializers.InstructorSerializer

class StudentViewSet(ModelViewSet):
    queryset = models.Student.objects.all()
    serializer_class = serializers.StudentSerializer  

class TutorViewSet(ModelViewSet):
    queryset = models.Tutor.objects.all()
    serializer_class = serializers.TutorSerializer  

class CategoryViewSet(ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer  

class AssignatureViewSet(ModelViewSet):
    queryset = models.Assignature.objects.all()
    serializer_class = serializers.AssignatureSerializer  

class ActivityViewSet(ModelViewSet):
    queryset = models.Activity.objects.all()
    serializer_class = serializers.ActivitySerializer  

class AtendanceViewSet(ModelViewSet):
    queryset = models.Atendance.objects.all()
    serializer_class = serializers.AtendanceSerializer  

class GradeViewSet(ModelViewSet):
    queryset = models.Grade.objects.all()
    serializer_class = serializers.GradeSerializer  

class QuarterGradeViewSet(ModelViewSet):
    queryset = models.QuarterGrade.objects.all()
    serializer_class = serializers.QuarterGradeSerializer  

class AnnouncementViewSet(ModelViewSet):
    queryset = models.Announcement.objects.all()
    serializer_class = serializers.AnnouncementSerializer  
