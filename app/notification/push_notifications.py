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

# from firebase_admin import messaging

# def send_push_notification(tokens, title, body, data=None):
#     """
#     Sends a push notification to one or multiple devices.
    
#     :param tokens: A single token (string) or a list of FCM device tokens
#     :param title: Notification title
#     :param body: Notification body
#     :param data: Optional dictionary with additional data
#     """

#     print('Device tokens:', tokens)

#     if not tokens:
#         print("No device tokens provided")
#         return {"success": False, "error": "No tokens"}

#     try:
#         # If only one token is passed as a string, convert it into a list
#         if isinstance(tokens, str):
#             tokens = [tokens]

#         # Use MulticastMessage to send notifications to multiple devices
#         message = messaging.MulticastMessage(
#             notification=messaging.Notification(
#                 title=title,
#                 body=body,
#             ),
#             data=data or {},  # Optional custom data payload
#             tokens=tokens,
#         )

#         response = messaging.send_multicast(message)
#         print(f"Successfully sent {response.success_count} messages out of {len(tokens)}")

#         return {
#             "success": True,
#             "success_count": response.success_count,
#             "failure_count": response.failure_count,
#             "responses": response.responses
#         }

#     except Exception as e:
#         print(f"Error sending messages: {e}")
#         return {"success": False, "error": str(e)}

