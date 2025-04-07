from celery import shared_task
from datetime import datetime, date
from django.utils import timezone
from django.db.models import Q
from django.core.cache import cache
from amauta.celery import app
import holidays
import pytz

from . import models
from notification.models import FCMDevice
from notification.push_notifications import send_push_notification

PERU_HOLIDAYS = holidays.Peru()

@shared_task
def mark_absent_students_in():
    """Mark students as absent."""
    schools = models.School.objects.all()

    for school in schools:

        today = timezone.localdate()

        if not models.Atendance.objects.filter(created_at__date=today, student__school=school).exists():
            print(f"Skipping school {school.id} (No attendance found for today)")
            continue

        classrooms = models.Clase.objects.filter(school=school)

        for classroom in classrooms:

            if not models.Atendance.objects.filter(
                created_at__date=today,
                student__clase=classroom,
            ).exists():
                print(f"Skipping classroom {classroom.id} (No entrance attendance found for today)")
                continue

            print(f'Marking absent students in classroom {classroom.id} for today')

            students = models.Student.objects.select_related('clase', 'school').prefetch_related('health_info', 'birth_info', 'emergency_contact', 'tutors', 'averages').filter(clase=classroom)
            print('students', students)
            for student in students:
                try:
                    models.Atendance.objects.get(
                        student=student,
                        kind='I',
                        created_at__date=date.today()
                    )

                    print(f"Student {student.uid} already have an attendance In for today")
                except:
                    models.Atendance.objects.create(
                        student=student,
                        status='N',
                        attendance_type='A',
                        kind='I',
                        created_by='System'
                    )
                    print(f"Student {student.uid} marked as absent at {datetime.now().isoformat()}")

@shared_task
def mark_on_time_students_out():

    if should_run_today():
        schools = models.School.objects.all()

        for school in schools:

            today = timezone.localdate()

            entrance_attendances = models.Atendance.objects.filter(
                created_at__date=today,
                kind="I",
                student__school=school,
            )

            created_count = 0 

            for attendance in entrance_attendances:
                student = attendance.student

                if attendance.status == "E":

                    if not models.Atendance.objects.filter(
                        student=student,
                        created_at__date=today,
                        kind="O"
                    ).exists():
                        # Create exit attendance
                        models.Atendance.objects.create(
                            created_at=today,
                            updated_at=today,
                            status="E",  
                            attendance_type="A",  
                            student=student,
                            created_by="System",
                            observations="",
                            kind="O"
                        )
                        created_count += 1

                elif attendance.status != "N":
                    if not models.Atendance.objects.filter(
                        student=student,
                        created_at__date=today,
                        kind="O"
                    ).exists():
                        models.Atendance.objects.create(
                            created_at=today,
                            updated_at=today,
                            status="O",
                            attendance_type="A",  
                            student=student,
                            created_by="System",
                            observations="",
                            kind="O"
                        )
                        created_count += 1
def should_run_today():
    """Check if the task should run today."""
    peru_timezone = pytz.timezone('America/Lima')
    today = datetime.now(peru_timezone)

    if today.weekday() in [5, 6]:
        return False
    
    return True

@shared_task
def run_if_valid_day():
    """Run the task if it's a valid day."""
    if should_run_today():
        mark_absent_students_in()
    else:
        print("Today is not a valid day to run the task.")



@shared_task
def remove_on_time_records():
    """Remove attendance with on time status from db."""
    if should_run_today():
        try:
            models.Atendance.objects.filter(
                status='O',
                created_at__date=date.today()
            ).delete()
            print("On time records removed")
        except: 
            print("No on time records to remove")
    else:
        print("Today is not a valid day to run the task.")

@shared_task
def send_activity_notification(users, activity_data, notification_title, update):
    print('sending activity notification')
    tokens = FCMDevice.objects.filter(user_id__in=users)
    print('tokens', tokens)
    message = f" {activity_data['title']} ha sido programada para el {activity_data['due_date']}"

    if update:
        message = f" {activity_data['title']} ha sido actualizada"
    for token in tokens:
        send_push_notification(token.device_token, notification_title, message)

@shared_task
def send_attendance_notification(users, notification_message, apologize_message=None):
    print('sending attendance notification')
    tokens = FCMDevice.objects.filter(user_id__in=users)
    message = ''
    if apologize_message:
        message = apologize_message
    else:
        message = notification_message

    for token in tokens:
            send_push_notification(token.device_token, 'Alerta de Asistencia', message)

@shared_task
def send_grade_notification(users, notification_message):
    print('sending grade notification')
    tokens = FCMDevice.objects.filter(user_id__in=users)
    message = notification_message

    for token in tokens:
            send_push_notification(token.device_token, 'Alerta de Notas', message)
