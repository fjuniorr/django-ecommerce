from django.test import SimpleTestCase
from django.test import SimpleTestCase
from sheetmusic.apps.integrations.adapter_key import AdapterKey


class AdapterKeyTests(SimpleTestCase):
    def test_fallback_sequence(self):
        key = AdapterKey.parse("shopify.na.subscription.recharge@s3#v2025_09:csv+gzip")
        self.assertEqual(
            key.fallback_candidates(),
            [
                "shopify.na.subscription.recharge@s3#v2025_09:csv+gzip",
                "shopify.na.subscription.recharge@s3#v2025_09:csv",
                "shopify.na.subscription.recharge@s3#v2025_09",
                "shopify.na.subscription.recharge@s3",
                "shopify.na.subscription.recharge",
                "shopify.na.subscription",
                "shopify.na.subscription",
                "shopify.na.*",
                "shopify.*",
                "*",
            ],
        )
