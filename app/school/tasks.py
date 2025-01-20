from celery import shared_task
from datetime import datetime, date
from django.core.cache import cache

from . import models

@shared_task
def mark_absent_students():
    """Mark students as absent."""
    today = date.today()
    students = models.Student.objects.select_related('clase')
    for student in students:
        cache_id = f"attendance_{student.uid}_I"
        attendance_in = cache.get(cache_id)
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
