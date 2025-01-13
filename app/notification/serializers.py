from rest_framework import serializers
from .models import FCMDevice

class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        fields = ['id', 'user', 'device_token', 'device_type']
        extra_kwargs = {
            'user': {'read_only': True} 
        }
