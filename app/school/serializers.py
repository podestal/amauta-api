from rest_framework import serializers
from . import models

class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Area
        fields = '__all__'

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.School
        fields = '__all__'

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Competence
        fields = '__all__'

class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Capacity
        fields = '__all__'

class ClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = '__all__'

class GetInstructorSerializer(serializers.ModelSerializer):

    class Meta: 
        model = models.Instructor
        fields = ['id', 'user', 'clases', 'first_name', 'last_name']

class CreateInstructorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Instructor
        fields = ['id', 'user', 'clases']

class GetAtendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'student', 'date', 'status', 'created_by', 'created_at', 'updated_at']

class CreateAtendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'student', 'status', 'created_by']

class GetStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['id', 'first_name', 'last_name', 'uid']

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['id', 'first_name', 'last_name', 'uid', 'clase']

class TutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutor
        fields = '__all__'

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

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Grade
        fields = '__all__'

class QuarterGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.QuarterGrade
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = '__all__'