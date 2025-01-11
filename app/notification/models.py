from django.db import models
from django.conf import settings

class PushSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="subscriptions")
    endpoint = models.URLField()
    auth = models.CharField(max_length=256)
    p256dh = models.CharField(max_length=256)

    def __str__(self):
        return f"Subscription for {self.user.username}"
