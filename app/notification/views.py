from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

from .models import PushSubscription

@csrf_exempt
@login_required
def save_subscription(request):
    if request.method == "POST":
        try:
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

            return JsonResponse({"success": True, "created": created})

        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({"success": False, "error": str(e)}, status=400)
    return JsonResponse({"success": False, "error": "Invalid request method"}, status=405)
