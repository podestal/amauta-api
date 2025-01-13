from django.urls import path
from .views import save_subscription, FCMDeviceView

urlpatterns = [
    path('save-subscription/', save_subscription, name='save-subscription'),
    path('fcm/register/', FCMDeviceView.as_view(), name='fcm-register'),
]
