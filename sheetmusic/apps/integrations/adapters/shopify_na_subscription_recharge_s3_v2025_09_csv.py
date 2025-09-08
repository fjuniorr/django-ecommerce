from ..registry import register
from ..base import BaseAdapter


@register("shopify.na.subscription.recharge@s3#v2025_09:csv")
class ShopifyRechargeFile(BaseAdapter):
    def identify_external_id(self, payload):
        return payload["id"]

    def normalize(self, payload, envelope):
        return {
            "provider": "shopify",
            "kind": "subscription",
            "channel": "recharge",
            "source_order_id": payload["id"],
            "currency": payload.get("currency", "USD"),
            "total": payload.get("total", "0"),
            "customer": {"external_id": payload.get("customer_id", "")},
            "lines": [
                {"sku": payload.get("sku", ""), "quantity": 1, "price": payload.get("total", "0")}
            ],
            "raw": payload,
        }
