from abc import ABC, abstractmethod
from .registry import register


class BaseAdapter(ABC):
    """Contract for all order normalization adapters.

    identify_external_id(payload) -> str
        Returns a provider-scoped unique id for the payload.

    normalize(payload, envelope) -> dict
        Returns canonical dict with keys:
        provider, kind, channel, program, source_order_id, currency,
        total, customer, lines, raw.

    persist(normalized) -> Order
        Performs idempotent upsert on (provider, source_order_id) and replaces lines.
    """

    @abstractmethod
    def identify_external_id(self, payload):
        ...

    @abstractmethod
    def normalize(self, payload, envelope):
        ...

    def persist(self, normalized):
        from sheetmusic.apps.ingest.models import Order, OrderLine, Customer

        customer_data = normalized.get("customer")
        customer = None
        if customer_data:
            customer, _ = Customer.objects.get_or_create(
                provider=normalized["provider"],
                external_id=customer_data["external_id"],
                defaults={"name": customer_data.get("name", "")},
            )
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
        order.lines.all().delete()
        for line in normalized.get("lines", []):
            OrderLine.objects.create(order=order, **line)
        return order
