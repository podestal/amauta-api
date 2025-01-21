from celery import shared_task
from datetime import datetime, date
from django.core.cache import cache
from amauta.celery import celery_app
import holidays
import pytz

from . import models

PERU_HOLIDAYS = holidays.Peru()

@shared_task
def mark_absent_students():
    """Mark students as absent."""
    students = models.Student.objects.select_related('clase')
    for student in students:
        cache_id = f"attendance_{student.uid}_I"
        print(f"Fetching cache for ID: {cache_id}")
        attendance_in = cache.get(cache_id)
        print(f"Cache result for {cache_id}: {attendance_in}")
        
        if not attendance_in:
            attendance = models.Atendance.objects.create(
                student=student,
                status='N',
                attendance_type='A',
                kind='I',
                created_by='System'
            )
            cache_data = {
                "id": attendance.id,
                "status": attendance.status,
                "kind": attendance.kind,
                "created_by": attendance.created_by,
                "observations": '',
                "created_at": datetime.now().isoformat(),
            }
            cache.set(cache_id, cache_data, timeout=54000)
            print(f"Student {student.uid} marked as absent at {datetime.now().isoformat()}")

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
