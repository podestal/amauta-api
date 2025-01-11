from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated
import json

from .models import PushSubscription

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

            subscription, created = PushSubscription.objects.update_or_create(
                user=user,
                defaults={
                    "endpoint": data["endpoint"],
                    "p256dh": data["keys"]["p256dh"],
                    "auth": data["keys"]["auth"],
                },
            )

            return Response({"success": True, "created": created})

        except (KeyError, json.JSONDecodeError) as e:
            return Response({"success": False, "error": str(e)}, status=400)
    return Response({"success": False, "error": "Invalid request method"}, status=405)
