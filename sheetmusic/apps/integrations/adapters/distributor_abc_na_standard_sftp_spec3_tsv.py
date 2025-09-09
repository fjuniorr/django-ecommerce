from ..registry import register
from ..base import BaseAdapter


@register("distributor_abc.na.standard@sftp#spec3:tsv")
class DistributorAbcFile(BaseAdapter):
    def identify_external_id(self, payload):
        return payload["id"]

    def normalize(self, payload, envelope):
        return {
            "provider": "distributor_abc",
            "kind": "standard",
            "source_order_id": payload["id"],
            "currency": payload.get("currency", "USD"),
            "total": payload.get("total", "0"),
            "customer": {"external_id": payload.get("customer_id", "")},
            "lines": [
                {"sku": payload.get("sku", ""), "quantity": 1, "price": payload.get("total", "0")}
            ],
            "raw": payload,
        }
