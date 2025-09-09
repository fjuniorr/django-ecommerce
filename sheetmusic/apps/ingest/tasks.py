from celery import shared_task
from celery.utils.log import get_task_logger
from .models import InboundEvent, InboundFile
from sheetmusic.apps.integrations.registry import resolve

logger = get_task_logger(__name__)


@shared_task
def process_inbound_event(event_id):
    event = InboundEvent.objects.get(id=event_id)
    try:
        adapter_cls = resolve(event.adapter_key)
    except KeyError:
        logger.warning("no adapter for %s", event.adapter_key)
        event.status = "adapter_missing"
        event.save(update_fields=["status"])
        return
    adapter = adapter_cls()
    normalized = adapter.normalize(event.raw_payload, {
        "flags": event.flags,
        "adapter_key": event.adapter_key,
    })
    adapter.persist(normalized)
    event.status = "processed"
    event.save(update_fields=["status"])


@shared_task
def poll_shopify_subscriptions_15m():
    """Demo periodic producer that enqueues a static payload."""
    payload = {"id": "demo-1", "total": "10.00", "currency": "USD"}
    env = {
        "adapter_key": "shopify.v2025_04.subscription.recharge",
        "transport": "http_api",
        "trigger": {"mode": "periodic", "schedule": "*/15 * * * *"},
        "flags": [],
    }
    event = InboundEvent.objects.create(
        adapter_key=env["adapter_key"],
        transport=env["transport"],
        trigger_mode=env["trigger"]["mode"],
        cursor=env.get("trigger", {}).get("cursor"),
        flags=env.get("flags", []),
        raw_payload=payload,
    )
    process_inbound_event.delay(str(event.id))


@shared_task
def demo_process_inbound_file_hourly():
    """Pretend to process a flat file periodically."""
    InboundFile.objects.create(
        provider="shopify",
        filename="demo.csv",
        checksum="demo",
        adapter_key_used="shopify.na.subscription.recharge@s3#v2025_09:csv",
        flags=["gzip"],
        manifest={"rows": 0},
        status="queued",
    )
