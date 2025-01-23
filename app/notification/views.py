# from django.http import JsonResponse
# from rest_framework.response import Response
# from rest_framework.decorators import api_view, permission_classes
# from django.views.decorators.csrf import csrf_exempt
# from rest_framework.permissions import IsAuthenticated
# import json

# from .models import PushSubscription

# @csrf_exempt
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def save_subscription(request):
#     print('save subscription ...')
#     if request.method == "POST":
#         try:
#             print('try ...')
#             data = json.loads(request.body)
#             user = request.user

#             subscription, created = PushSubscription.objects.update_or_create(
#                 user=user,
#                 defaults={
#                     "endpoint": data["endpoint"],
#                     "p256dh": data["keys"]["p256dh"],
#                     "auth": data["keys"]["auth"],
#                 },
#             )

#             return Response({"success": True, "created": created})

#         except (KeyError, json.JSONDecodeError) as e:
#             return Response({"success": False, "error": str(e)}, status=400)
#     return Response({"success": False, "error": "Invalid request method"}, status=405)

from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
import json

from .models import PushSubscription, FCMDevice
from .serializers import FCMDeviceSerializer

@csrf_exempt
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_subscription(request):
    print('save subscription ...')
    if request.method == "POST":
        try:
            print('try ...')
            data = json.loads(request.body)
            user = request.user

            subscription = PushSubscription.objects.create(
                user=user,
                endpoint=data["endpoint"],
                p256dh=data["keys"]["p256dh"],
                auth=data["keys"]["auth"],
            )

            return Response({"success": True, "created": True})

        except (KeyError, json.JSONDecodeError) as e:
            return Response({"success": False, "error": str(e)}, status=400)
    return Response({"success": False, "error": "Invalid request method"}, status=405)



class FCMDeviceView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = FCMDeviceSerializer(data=request.data)
        if serializer.is_valid():
            device_token = serializer.validated_data['device_token']
            device_type = serializer.validated_data.get('device_type', 'unknown')

            # Remove the existing device token if it's already linked to another user
            FCMDevice.objects.filter(device_token=device_token).exclude(user=request.user).delete()

            # Update or create the device token for the current user
            fcm_device, created = FCMDevice.objects.update_or_create(
                user=request.user,
                device_token=device_token,
                defaults={'device_type': device_type}
            )

            return Response(
                {
                    "message": "Device token registered successfully",
                    "created": created,
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

