from ..registry import register
from ..base import BaseAdapter


@register("shopify.v2025_04.subscription.recharge", "shopify.v2025_04.subscription")
class ShopifyRecharge(BaseAdapter):
    def identify_external_id(self, payload):
        return payload["id"]

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
