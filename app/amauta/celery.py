import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amauta.settings')

app = Celery('amauta')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.timezone = 'America/Lima'
broker_connection_retry_on_startup = True
# celery_app.autodiscover_tasks()
app.autodiscover_tasks(['school'])

app.conf.beat_schedule = {
    'run_task_everyday_at_9am': {
        'task': 'school.tasks.run_if_valid_day',
        'schedule': crontab(hour=10, minute=00),

    },
    'run_task_everyday_at_midnigth': {
        'task': 'school.tasks.mark_on_time_students_out',
        'schedule': crontab(hour=16, minute=00),
    }
}
