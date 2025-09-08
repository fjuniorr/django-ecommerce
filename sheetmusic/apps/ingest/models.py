import uuid
from django.db import models


class InboundEvent(models.Model):
    """Inbound payload from any transport/trigger.

    Stores raw payload and envelope metadata for idempotent processing and replay.
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adapter_key = models.CharField(max_length=255)
    transport = models.CharField(max_length=32)
    trigger_mode = models.CharField(max_length=32)
    cursor = models.JSONField(null=True, blank=True)
    flags = models.JSONField(default=list, blank=True)
    raw_payload = models.JSONField()
    status = models.CharField(max_length=32, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["adapter_key", "status"]),
            models.Index(fields=["transport", "trigger_mode"]),
        ]


class InboundFile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    provider = models.CharField(max_length=64)
    filename = models.CharField(max_length=255)
    checksum = models.CharField(max_length=64)
    adapter_key_used = models.CharField(max_length=255)
    flags = models.JSONField(default=list, blank=True)
    manifest = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=32, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Customer(models.Model):
    provider = models.CharField(max_length=64)
    external_id = models.CharField(max_length=64)
    name = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ("provider", "external_id")


class Order(models.Model):
    provider = models.CharField(max_length=64)
    source_order_id = models.CharField(max_length=64)
    currency = models.CharField(max_length=8)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True, blank=True)
    raw = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ("provider", "source_order_id")


class OrderLine(models.Model):
    order = models.ForeignKey(Order, related_name="lines", on_delete=models.CASCADE)
    sku = models.CharField(max_length=64)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
