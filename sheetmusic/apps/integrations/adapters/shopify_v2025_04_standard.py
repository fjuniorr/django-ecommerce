from ..registry import register
from ..base import BaseAdapter


@register("shopify.v2025_04.standard")
class ShopifyStandard(BaseAdapter):
    def identify_external_id(self, payload):
        return payload["id"]

    def normalize(self, payload, envelope):
        return {
            "provider": "shopify",
            "kind": "standard",
            "source_order_id": payload["id"],
            "currency": payload.get("currency", "USD"),
            "total": payload.get("total", "0"),
            "customer": {"external_id": payload.get("customer_id", "")},
            "lines": [
                {"sku": "demo", "quantity": 1, "price": payload.get("total", "0")}
            ],
            "raw": payload,
        }
