# import json
# from pywebpush import webpush, WebPushException
# import os

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
#             vapid_private_key=VAPID_PRIVATE_KEY,  # Pass the private key as a string
#             vapid_claims=VAPID_CLAIMS,
#         )
#         print("Notification sent!")
#     except WebPushException as e:
#         print(f"WebPush Error: {e}")
#     except ValueError as e:
#         print(f"Value Error: {e}")

from firebase_admin import messaging

def send_push_notification(token, title, body, data=None):
    """
    Sends a push notification to the specified device.
    
    :param token: FCM device token
    :param title: Notification title
    :param body: Notification body
    :param data: Optional dictionary with additional data
    """

    print('device token', token)
    try:
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},  # Optional custom data payload
            token=token,
        )
        response = messaging.send(message)
        print(f"Successfully sent message: {response}")
        return {"success": True, "response": response}
    except Exception as e:
        print(f"Error sending message: {e}")
        return {"success": False, "error": str(e)}
