from django.db import models
from django.conf import settings

class PushSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    endpoint = models.URLField()
    auth = models.CharField(max_length=256)
    p256dh = models.CharField(max_length=256)

    def __str__(self):
        return f"Subscription for {self.user.username}"

# class FCMDevice(models.Model):
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL, 
#         on_delete=models.CASCADE,
#         related_name="fcm_devices"
#     )
#     device_token = models.CharField(max_length=255, unique=True)
#     device_type = models.CharField(max_length=50, blank=True, null=True)  # e.g., "android", "ios", "web"
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.user.username} - {self.device_type}"