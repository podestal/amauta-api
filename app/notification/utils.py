
from . import models
from . import push_notifications

def get_notification_message_attendance(self, student, status):

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


def send_notification(self, student, tutor, status, apologize_message=None):

    print('sending attendance notification')
    tokens = models.FCMDevice.objects.filter(user=tutor.user)
    message = ''
    if apologize_message:
        message = apologize_message
    else:
        message = self.get_notification_message(student, status)

    for token in tokens:
            push_notifications.send_push_notification(token.device_token, 'Alerta de Asistencia', message)

def send_activity_notification(users, activity, notification_title):

    print('sending activity notification')
    print('activity', activity)
    tokens = models.FCMDevice.objects.filter(user_id__in=users)
    message = f" {activity['title']} ha sido programada para el {activity['due_date']}"
    for token in tokens:
        push_notifications.send_push_notification(token.device_token, notification_title, message)