# Tutorial: Ingesting and Normalizing Orders

This tutorial demonstrates how Sheetmusic ingests raw data from various sources and normalizes it into a canonical order model.

## Capture an inbound event

Inbound events from webhooks, APIs, or scheduled polls are stored with an adapter key and envelope metadata:

```python
from sheetmusic.apps.ingest.models import InboundEvent
from sheetmusic.apps.ingest.tasks import process_inbound_event

payload = {"id": "demo-1", "total": "10.00", "currency": "USD"}
env = {
    "adapter_key": "shopify.v2025_04.subscription.recharge",
    "transport": "http_api",
    "trigger": {"mode": "periodic"},
    "flags": [],
}

event = InboundEvent.objects.create(
    adapter_key=env["adapter_key"],
    transport=env["transport"],
    trigger_mode=env["trigger"]["mode"],
    raw_payload=payload,
)
process_inbound_event.delay(str(event.id))
```

## Trigger ingestion jobs

Celery workers pull tasks from a Redis queue. Jobs can be enqueued manually or
on a schedule.

### Manual trigger

From the Django shell you can enqueue a task directly:

```python
from sheetmusic.apps.ingest.tasks import poll_shopify
poll_shopify.delay()
```

### Scheduled with Celery beat

`CELERY_BEAT_SCHEDULE` defines periodic tasks that Celery beat enqueues
automatically:

```python
from celery.schedules import crontab

CELERY_BEAT_SCHEDULE = {
    "poll-shopify": {
        "task": "sheetmusic.apps.ingest.tasks.poll_shopify",
        "schedule": crontab(minute="*/15"),
    },
}
```

## Resolve an adapter

The adapter key identifies which normalization adapter should handle the event. Resolution falls back from most to least specific using `AdapterKey`:

```python
from sheetmusic.apps.integrations.registry import resolve
adapter_cls = resolve(event.adapter_key)
adapter = adapter_cls()
```

## Normalize and persist

Adapters subclass `BaseAdapter` and implement `normalize` to convert raw payloads into canonical orders. The ingestion task calls `normalize` and then `persist`:

```python
@register("shopify.v2025_04.subscription.recharge")
class ShopifyRecharge(BaseAdapter):
    def normalize(self, payload, envelope):
        lines = [
            {"sku": "bundle", "quantity": 1, "price": payload.get("total", "0")}
        ]
        if "split-bundles" in envelope.get("flags", []):
            lines = [
                {"sku": "component1", "quantity": 1, "price": payload.get("total", "0")},
                {"sku": "component2", "quantity": 1, "price": "0"}
            ]
        return {
            "provider": "shopify",
            "kind": "subscription",
            "channel": "recharge",
            "source_order_id": payload["id"],
            "currency": payload.get("currency", "USD"),
            "total": payload.get("total", "0"),
            "customer": {"external_id": payload.get("customer_id", "")},
            "lines": lines,
            "raw": payload,
        }
```

`BaseAdapter.persist` upserts the canonical order and replaces any existing lines:

```python
order, _ = Order.objects.update_or_create(
    provider=normalized["provider"],
    source_order_id=normalized["source_order_id"],
    defaults={
        "currency": normalized["currency"],
        "total": normalized["total"],
        "customer": customer,
        "raw": normalized.get("raw", {}),
    },
)
```

## Adding a new adapter

To integrate another provider or channel:

1. Implement a subclass of `BaseAdapter` with `identify_external_id` and `normalize`.
2. Decorate the class with `@register(<adapter_key>)`.
3. Use envelope flags, formats, or schema versions to differentiate behaviors.

This pattern decouples transport concerns from semantic normalization, enabling straightforward ingestion of new sources.

## Technical annex: Redis queues

Celery uses Redis as its message broker and result backend. Tasks pushed with
`delay` or scheduled by beat are stored in Redis lists keyed by queue name.

During development you can inspect the queues with `redis-cli`:

```bash
# show number of pending jobs on default queue
redis-cli -n 0 llen celery

# inspect job payloads waiting on the queue
redis-cli -n 0 lrange celery 0 -1
```

These commands help verify that events are enqueued and shaped correctly before
workers process them.

