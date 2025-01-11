# import json
# import os
# from pywebpush import webpush, WebPushException

# VAPID_PRIVATE_KEY = os.environ.get("VAPID_PRIVATE_KEY")
# VAPID_PUBLIC_KEY = os.environ.get("VAPID_PUBLIC_KEY")
# VAPID_CLAIMS = {
#     "sub": "mailto:l.r.p.2991@gmail.com",
# }

# def send_push_notification(subscription, title, body, url=None):
#     payload = {
#         "title": title,
#         "body": body,
#         "url": url,
#     }

#     try:
#         webpush(
#             subscription_info={
#                 "endpoint": subscription.endpoint,
#                 "keys": {
#                     "p256dh": subscription.p256dh,
#                     "auth": subscription.auth,
#                 },
#             },
#             data=json.dumps(payload),
#             vapid_private_key=VAPID_PRIVATE_KEY,
#             vapid_claims=VAPID_CLAIMS,
#         )
#         print("Notification sent!")
#     except WebPushException as e:
#         print(f"WebPush Error: {e}")


# def mark_student_absent(student):
#     # Mark the student as absent in the database
#     student.attendance_status = "Absent"
#     student.save()

#     # Send a push notification to the student's tutor
#     subscription = PushSubscription.objects.get(user=student.tutor)
#     send_push_notification(
#         subscription,
#         title="Attendance Alert",
#         body=f"{student.first_name} {student.last_name} was marked absent.",
#         url="/attendance-details",
#     )