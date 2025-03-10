from celery import shared_task
from datetime import datetime, date
from django.core.cache import cache
from amauta.celery import celery_app
import holidays
import pytz

from . import models
from notification.models import FCMDevice
from notification.push_notifications import send_push_notification

PERU_HOLIDAYS = holidays.Peru()

@shared_task
def mark_absent_students():
    """Mark students as absent."""
    students = models.Student.objects.select_related('clase')
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

    # Using Cache memroy to store the attendance
    # students = models.Student.objects.select_related('clase')
    # for student in students:
    #     cache_id = f"attendance_{student.uid}_I"
    #     print(f"Fetching cache for ID: {cache_id}")
    #     attendance_in = cache.get(cache_id)
    #     print(f"Cache result for {cache_id}: {attendance_in}")
        
    #     if not attendance_in:
    #         attendance = models.Atendance.objects.create(
    #             student=student,
    #             status='N',
    #             attendance_type='A',
    #             kind='I',
    #             created_by='System'
    #         )
    #         cache_data = {
    #             "id": attendance.id,
    #             "status": attendance.status,
    #             "kind": attendance.kind,
    #             "created_by": attendance.created_by,
    #             "observations": '',
    #             "created_at": datetime.now().isoformat(),
    #         }
    #         cache.set(cache_id, cache_data, timeout=54000)
    #         print(f"Student {student.uid} marked as absent at {datetime.now().isoformat()}")

def should_run_today():
    """Check if the task should run today."""
    peru_timezone = pytz.timezone('America/Lima')
    today = datetime.now(peru_timezone)

    if today.weekday() in [5, 6]:
        return False

    if today.date() in PERU_HOLIDAYS:
        return False
    
    return True

@shared_task
def run_if_valid_day():
    """Run the task if it's a valid day."""
    if should_run_today():
        mark_absent_students()
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

