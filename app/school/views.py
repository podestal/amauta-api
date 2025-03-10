from datetime import date
from unidecode import unidecode
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.db.models.functions import ExtractWeek, ExtractMonth, ExtractDay
from django.utils import timezone
from datetime import timedelta
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, IsAuthenticated
from django.db.models import Subquery, OuterRef, Prefetch
from django.core.cache import cache
from datetime import datetime

import pandas as pd
import openpyxl
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from notification.push_notifications import send_push_notification
from . import tasks
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

    def update(self, request, *args, **kwargs):
        print('request', request.data)

        status = request.data['status']
        kind = request.data['kind']
        student_id = request.data['student']
        student = models.Student.objects.get(uid=student_id)
    
        if not student: 
            return Response({"error": "No se pudo encontrar alumno"}, status=400)
        notification_message = self.get_notification_message(student, status)
        try:
            users = models.Tutor.objects.filter(students__uid=student_id).values_list('user', flat=True)
            # def send_attendance_notification(users, notification_message, apologize_message=None):
        except:
            print('could not find users')
        tasks.send_attendance_notification.delay(list(users), notification_message, apologize_message=f'{student.first_name} llegó a tiempo')
        return super().update(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        print('data', request.data)
        status = request.data['status']
        kind = request.data['kind']
        student_id = request.data['student']

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
            notification_message = self.get_notification_message(student, status)
            try:
                users = models.Tutor.objects.filter(students__uid=student_id).values_list('user', flat=True)
            except:
                # attendance_id = super().create(request, *args, **kwargs).data['id']
                # cache = self.save_to_cache(student, kind, status, request, attendance_id=attendance_id)
                # return Response(cache, status=201)
                print('could not find users')
                return super().create(request, *args, **kwargs)
            
            # self.send_notification(student, tutor, status)
            tasks.send_attendance_notification.delay(list(users), notification_message)
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
                    Prefetch('atendances', queryset=attendance_out, to_attr='attendance_out'),
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
        competencies = request.query_params.get('competencies').split(',')
        competencies = [c for c in competencies if c]
        quarter = request.query_params.get('quarter')
        students = self.get_queryset().filter(clase=clase)
        students = students.prefetch_related(
            Prefetch(
                "averages",
                queryset=models.QuarterGrade.objects.filter(
                    quarter=quarter,
                    competence__in=competencies
                ),
                to_attr="filtered_averages"
            )
        )
        serializer = serializers.GetStudentForQuarterGradeSerializer(students, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def byGrade(self, request):
        clase = request.query_params.get('clase')
        competence = request.query_params.get('competence')
        quarter = request.query_params.get('quarter')
        students = self.get_queryset().filter(clase=clase)
        students = students.prefetch_related(
            Prefetch(
                "grades",
                queryset=models.Grade.objects.filter(
                    activity__competences=competence,
                    activity__quarter=quarter
                )
                .select_related('activity', 'activity__category', 'assignature')
                .prefetch_related('activity__competences'),
                to_attr="filtered_grades"
            ),
            Prefetch(
                "averages",
                queryset=models.QuarterGrade.objects.filter(
                    quarter=quarter
                ),
                to_attr="filtered_averages"
            )
        )

        serializer = serializers.GetStudentForFilteredGradesSerializer(students, many=True)
        return Response(serializer.data)
    
    # @action(detail=False, methods=["get"])
    # def export_to_excel(self, request):
    #     # Fetch data from model
    #     data = list(models.Student.objects.values("uid", "first_name", "last_name"))  # Adjust fields
    #     df = pd.DataFrame(data)

    #     # Create an HTTP response
    #     response = HttpResponse(
    #         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )
    #     response["Content-Disposition"] = 'attachment; filename="students.xlsx"'

    #     # Save the DataFrame to the response
    #     with pd.ExcelWriter(response, engine="openpyxl") as writer:
    #         df.to_excel(writer, sheet_name="Students", index=False)

    #     return response
    # @action(detail=False, methods=["get"])
    # def export_to_excel(self, request):
    #     # Create a new workbook and remove the default sheet
    #     wb = Workbook()
    #     wb.remove(wb.active)

    #     # Define data sources (Adjust fields as needed)
    #     student_data = list(models.Student.objects.values("uid", "first_name", "last_name"))
    #     instructor_data = list(models.Instructor.objects.values("id", "first_name", "last_name"))

    #     # Convert to DataFrame
    #     df_students = pd.DataFrame(student_data)
    #     df_instructors = pd.DataFrame(instructor_data)

    #     # Add sheets and write data
    #     self.write_to_sheet(wb, df_students, "Students")
    #     self.write_to_sheet(wb, df_instructors, "Instructors")

    #     # Prepare response
    #     response = HttpResponse(
    #         content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    #     )
    #     response["Content-Disposition"] = 'attachment; filename="school_data.xlsx"'

    #     # Save workbook to response
    #     wb.save(response)
    #     return response

    # def write_to_sheet(self, wb, df, sheet_name):
    #     sheet = wb.create_sheet(title=sheet_name)

    #     # Write headers with styling
    #     header_font = Font(bold=True)
    #     for col_num, column_title in enumerate(df.columns, 1):
    #         cell = sheet.cell(row=1, column=col_num, value=column_title)
    #         cell.font = header_font
    #         cell.alignment = Alignment(horizontal="center")

    #     # Write data rows
    #     for row_num, row in enumerate(df.itertuples(index=False), 2):
    #         for col_num, value in enumerate(row, 1):
    #             sheet.cell(row=row_num, column=col_num, value=value)

    #     # Auto-adjust column width
    #     for col in sheet.columns:
    #         max_length = max(len(str(cell.value)) if cell.value else 0 for cell in col)
    #         sheet.column_dimensions[col[0].column_letter].width = max_length + 2

    @action(detail=False, methods=["get"])
    def export_to_excel(self, request):

        quarter_description = {
            'Q1': 'Primer Bimestre',
            'Q2': 'Segundo Bimestre',
            'Q3': 'Tercer Bimestre',
            'Q4': 'Cuarto Bimestre',
        }


        classroom_grade_converter = {
            '1': 'Primero',
            '2': 'Segundo',
            '3': 'Tercero',
            '4': 'Cuarto',
            '5': 'Quinto',
            '6': 'Sexto',
        }

        classroom_level_converter = {
            'I': 'Inicial',
            'P': 'Primaria',
            'S': 'Secundaria',
        }


        # Create a workbook and rename the default sheet
        classroom = request.query_params.get('classroom')
        quarter= request.query_params.get('quarter')
        instructor_id = request.query_params.get('instructor_id')

        clase = get_object_or_404(models.Clase, id=classroom)
        classroom_section = clase.section if clase.section else ''
        if classroom_section == 'U':
            classroom_section = 'Única'
        classroom_grade = clase.grade if clase.grade else ''
        classroom_level = clase.level if clase.level else ''

        wb = openpyxl.Workbook()
        ws_general = wb.active
        ws_general.title = "Generalidades"

        # Define border style
        thin_border = Border(left=Side(style="thin"), right=Side(style="thin"), 
                            top=Side(style="thin"), bottom=Side(style="thin"))

        header_fill = PatternFill(start_color="000066", end_color="000066", fill_type="solid")
        header_font = Font(bold=True, color="FFFFFF")

        # Format "DATOS GENERALES"
        ws_general["B2"] = "DATOS GENERALES :"
        ws_general["B2"].font = Font(bold=True, size=12)
        
        # "Institución Educativa" from B to J
        ws_general["B4"] = "Institución Educativa :"
        ws_general.merge_cells("B4:J4")
        ws_general["B4"].fill = header_fill
        ws_general["B4"].font = header_font
        ws_general["B4"].alignment = Alignment(horizontal="center")

        # "Código Modular - Anexo" from B to D
        ws_general["B5"] = "Código Modular - Anexo :"
        ws_general.merge_cells("B5:D5")
        ws_general.merge_cells("E5:F5")

        # "Nivel" at G, with space from H to J
        ws_general["G5"] = "Nivel :"
        ws_general['H5'] = f'{classroom_level_converter[classroom_level]}'
        ws_general.merge_cells("H5:J5")

        # "Nombre" at B, space from C to J
        ws_general["B6"] = "Nombre :"
        ws_general.merge_cells("B6:J6")

        # "Datos referentes al Registro de Notas" from B to J
        ws_general["B7"] = "Datos referentes al Registro de Notas :"
        ws_general.merge_cells("B7:J7")
        ws_general["B7"].fill = header_fill
        ws_general["B7"].font = header_font
        ws_general["B7"].alignment = Alignment(horizontal="center")

        # "Año Académico" from B to C, "2019" from D to J
        ws_general["B8"] = "Año Académico :"
        ws_general.merge_cells("B8:C8")
        ws_general["D8"] = "2025"
        ws_general.merge_cells("D8:J8")

        # "Diseño Curricular" from B to C, value from D to J
        ws_general["B9"] = "Diseño Curricular :"
        ws_general.merge_cells("B9:C9")
        ws_general["D9"] = "CURRÍCULO NACIONAL 2017"
        ws_general.merge_cells("D9:J9")

        # "Grado" from B to C, space from D to E, "Sección" at F, space from G to J
        ws_general["B10"] = "Periodo de evaluación :"
        ws_general.merge_cells("B10:C10")
        ws_general["D10"] = f"{quarter_description[quarter]}"
        ws_general.merge_cells("D10:F10")
        ws_general["G10"] = "Grado"
        ws_general["H10"] = f'{classroom_grade_converter[classroom_grade]}'
        ws_general["I10"] = "Sección"
        ws_general["J10"] = f'{classroom_section}'

        # Apply borders from B2 to J10
        for row in ws_general.iter_rows(min_row=4, max_row=10, min_col=2, max_col=10):
            for cell in row:
                cell.border = thin_border

        # "AREAS" Section
        ws_general["B13"] = "AREAS"
        ws_general["B13"].font = Font(bold=True)
        areas_ids = models.Assignature.objects.filter(clase=classroom,instructor=instructor_id).values_list('area_id', flat=True)
        # List areas from model in column B (ID) and column C (Title)
        areas = models.Area.objects.filter(id__in=areas_ids)
        row = 14
        for area in areas:
            ws_general[f"B{row}"] = area.id
            ws_general[f"C{row}"] = area.title
            row += 1

        competences = models.Competence.objects.select_related('area')
        students = self.get_queryset().filter(clase=classroom)  
        students = students.prefetch_related(
            Prefetch(
                "averages",
                queryset=models.QuarterGrade.objects.filter(
                    quarter='Q1',
                ),
                to_attr="filtered_averages"
            ))

        # Create separate sheets for each area
        for area in areas[:11]:  # Limit to 11 additional sheets
            ws_area = wb.create_sheet(title=area.title)
            ws_area["A1"] = 'ID'
            ws_area["A1"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
            ws_area['A1'].font = Font(bold=True, color="FFFFFF")
            ws_area['A1'].alignment = Alignment(horizontal="center",  vertical="center")
            ws_area['B1'].font = Font(bold=True, color="FFFFFF")
            ws_area.merge_cells("A1:A2")

            ws_area["B1"] = 'Cod. Estudiante'
            ws_area["B1"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
            ws_area["B1"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
            ws_area['B1'].alignment = Alignment(horizontal="center", vertical="center")
            ws_area.merge_cells("B1:B2")

            ws_area["C1"] = 'Nombres'
            ws_area["C1"].font = Font(bold=True, color="FFFFFF")
            ws_area["C1"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
            ws_area['C1'].alignment = Alignment(horizontal="center", vertical="center")
            ws_area.merge_cells("C1:C2")

            filtered_competences = competences.filter(area=area)

            start_col = 4 
            start_row = 1
            description_row = 2

            for index, competence in enumerate(filtered_competences, start=1):
                col_letter = get_column_letter(start_col)  # Get letter for merging
                next_col_letter = get_column_letter(start_col + 1)  # Next column for merging
                
                # Set the competence number
                ws_area[f"{col_letter}{start_row}"] = f"{index:02d}"  # Format 01, 02, etc.
                ws_area[f"{col_letter}{start_row}"].font = Font(bold=True, color="FFFFFF")
                ws_area[f"{col_letter}{start_row}"].alignment = Alignment(horizontal="center", vertical="center")
                ws_area[f"{col_letter}{start_row}"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")
                ws_area.merge_cells(f"{col_letter}{start_row}:{next_col_letter}{start_row}")  # Merge columns

                # Set the 'NL' label
                ws_area[f"{col_letter}{description_row}"] = "NL"
                ws_area[f"{col_letter}{description_row}"].font = Font(bold=True, color="FFFFFF")
                ws_area[f"{col_letter}{description_row}"].alignment = Alignment(horizontal="center", vertical="center")
                ws_area[f"{col_letter}{description_row}"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")

                # Set the description header
                ws_area[f"{next_col_letter}{description_row}"] = "Conclusión descriptiva de la competencia"
                ws_area[f"{next_col_letter}{description_row}"].font = Font(bold=True, color="FFFFFF")
                ws_area[f"{next_col_letter}{description_row}"].alignment = Alignment(horizontal="center", vertical="center")
                ws_area[f"{next_col_letter}{description_row}"].fill = PatternFill(start_color="808080", end_color="808080", fill_type="solid")

                # Move to the next pair of columns
                start_col += 2
            
            start_row = 3
            for student in students:
                ws_area[f"A{start_row}"] = student.uid
                ws_area[f"B{start_row}"] = '0000004567'
                ws_area[f"C{start_row}"] = f"{student.first_name} {student.last_name}"
                    # Start placing grades and conclusions dynamically
                col = 4  # Start at first competence column
                for competence in filtered_competences:
                    col_letter = get_column_letter(col)
                    next_col_letter = get_column_letter(col + 1)

                    # Find the grade and conclusion for this competence
                    grade = ''
                    conclusion = ''
                    for avg in student.filtered_averages:
                        if avg.competence_id == competence.id:  # Match competence ID
                            grade = avg.calification
                            conclusion = avg.conclusion
                            break  # Stop once found
                    
                    # Insert the grade
                    ws_area[f"{col_letter}{start_row}"] = grade if grade else "NA"
                    ws_area[f"{col_letter}{start_row}"].alignment = Alignment(horizontal="left")

                    # Insert the conclusion
                    ws_area[f"{next_col_letter}{start_row}"] = conclusion if conclusion else ""
                    ws_area[f"{next_col_letter}{start_row}"].alignment = Alignment(horizontal="left", wrap_text=True)

                    col += 2  # Move to next competence column

                start_row += 1  # Move to the next student row


            ws_area[f"B{len(students) + 4}"] = 'LEYENDA'
            ws_area[f"B{len(students) + 4}"].font = Font(bold=True)

            ws_area[f"B{len(students) + 5}"] = 'NL= Nivel de logro alcanzado'
            ws_area.merge_cells(f"B{len(students) + 5}:C{len(students) + 5}")

            competence_start_row = len(students) + 6 

            for index, competence in enumerate(filtered_competences, start=1):
                row_number = competence_start_row + index - 1
                ws_area[f"B{row_number}"] = f"{index:02d}={competence.title}"  # Format: 01=Title
                ws_area.merge_cells(f"B{row_number}:C{row_number}")  # Merge B and C for better readability


            # Auto-adjust column width
            for col in ws_area.columns:
                max_length = 0
                col_letter = get_column_letter(col[0].column)
                
                for cell in col:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                
                ws_area.column_dimensions[col_letter].width = max_length + 2

            for row in ws_area.iter_rows(min_row=1, max_row=start_row-1, min_col=1, max_col=3+(2*len(filtered_competences))):
                for cell in row:
                    cell.border = thin_border

        # Prepare response
        response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="data.xlsx"'
        
        # Save the workbook to the response
        wb.save(response)
        
        return response
    

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
    
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except:
            raise ValidationError("Esta categoría no puede ser eliminada porque tiene actividades asociadas.")
    
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
        competence = request.query_params.get('competence')
        quarter = request.query_params.get('quarter')
        if not assignature:
            return Response({"error": "Assignature parameter is required"}, status=400)
        activities = self.queryset.filter(assignature_id=assignature, quarter=quarter)
        if competence:
            activities = activities.filter(competences=competence)
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

    def create(self, request, *args, **kwargs):

        classroom = request.query_params.get('classroom')
        students_uids = models.Student.objects.filter(clase=classroom).values_list('uid', flat=True)
        users = models.Tutor.objects.filter(students__in=students_uids).values_list('user', flat=True)
        print('users', users)
        activity = super().create(request, *args, **kwargs)
        # print('activity', activity.data)
        tasks.send_activity_notification.delay(list(users), activity.data, 'Nueva Actividad', False)
        return activity
    
    def update(self, request, *args, **kwargs):
        classroom = request.query_params.get('classroom')
        students_uids = models.Student.objects.filter(clase=classroom).values_list('uid', flat=True)
        users = models.Tutor.objects.filter(students__in=students_uids).values_list('user', flat=True)
        print('users', users)
        activity = super().update(request, *args, **kwargs)
        tasks.send_activity_notification.delay(list(users), activity.data, 'Cambios en actividad', True)
        return activity
    
    

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
    
    def update(self, request, *args, **kwargs):
        student_id = self.request.query_params.get('student_uid')
        student = models.Student.objects.get(uid=student_id)
        users = models.Tutor.objects.filter(students__uid=student_id).values_list('user', flat=True)
        notification_message = f'{student.first_name} ha recibido una nueva calificación'
        tasks.send_grade_notification.delay(list(users), notification_message)
        return super().update(request, *args, **kwargs)

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
