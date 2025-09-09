import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import InboundEvent
from .tasks import process_inbound_event


@csrf_exempt
def webhook(request):
    envelope = json.loads(request.body)
    event = InboundEvent.objects.create(
        adapter_key=envelope["adapter_key"],
        transport=envelope["transport"],
        trigger_mode=envelope.get("trigger", {}).get("mode", "push"),
        cursor=envelope.get("trigger", {}).get("cursor"),
        flags=envelope.get("flags", []),
        raw_payload=envelope.get("payload", {}),
    )
    process_inbound_event.delay(str(event.id))
    return JsonResponse({}, status=202)
