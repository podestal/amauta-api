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
        fields = ['id']

class CompetenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Competence
        fields = '__all__'

class CapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Capacity
        fields = '__all__'

class GetClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section', 'students']

class GetSimpleClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section']

class CreateClaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Clase
        fields = ['id', 'grade', 'level', 'section']

class GetInstructorSerializer(serializers.ModelSerializer):

    clases_details = serializers.SerializerMethodField()

    class Meta: 
        model = models.Instructor
        fields = ['id', 'user', 'clases_details', 'first_name', 'last_name']

    def get_clases_details(self, obj):
        return [
            f"{clase.grade}-{clase.section}-{clase.level}-{clase.id}"
            for clase in obj.clases.all()
        ]

class CreateInstructorSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Instructor
        fields = ['id', 'user', 'clases']

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
        fields = ['id', 'status', 'observations', 'kind']

class CreateAtendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Atendance
        fields = ['id', 'student', 'status', 'created_by', 'observations', 'attendance_type', 'kind']

class GetStudentSerializer(serializers.ModelSerializer):

    attendances = serializers.SerializerMethodField()

    class Meta:
        model = models.Student
        fields = ['first_name', 'last_name', 'uid', 'attendances', 'tutor_phone']

    def get_attendances(self, obj):

        in_key = f"attendance_{obj.uid}_I"
        out_key = f"attendance_{obj.uid}_O"

        attendances_in = cache.get(in_key)
        attendances_out = cache.get(out_key)
        
        return {
            "In": attendances_in if attendances_in is not None else "",
            "Out": attendances_out if attendances_out is not None else ""
        }
    
class GetStudentForTutorSerializer(serializers.ModelSerializer):

    clase = GetSimpleClaseSerializer()
    attendances = serializers.SerializerMethodField()

    class Meta: 
        model = models.Student
        fields = ['first_name', 'last_name', 'uid', 'clase', 'attendances']

    def get_attendances(self, obj):
        return models.Atendance.objects.filter(student=obj.uid).values('status', 'created_at', 'observations')

class CreateStudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Student
        fields = ['first_name', 'last_name', 'uid', 'clase','tutor_phone']

class GetTutorSerializer(serializers.ModelSerializer):

    students = GetStudentForTutorSerializer(many=True)

    class Meta:
        model = models.Tutor
        fields = ['id', 'students', 'first_name', 'last_name', 'phone_number', 'address', 'email', 'can_access']

class CreateTutorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Tutor
        fields = ['id', 'user', 'students', 'first_name', 'last_name', 'phone_number', 'address', 'email']


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

class GetAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ['id', 'title', 'description', 'created_at', 'student', 'created_by']

class CreateAnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Announcement
        fields = ['id', 'title', 'description', 'student', 'created_by']