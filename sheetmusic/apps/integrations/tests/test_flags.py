from django.test import SimpleTestCase
from sheetmusic.apps.integrations.adapters.shopify_v2025_04_subscription_recharge import ShopifyRecharge


class FlagTests(SimpleTestCase):
    def test_flags_modify_normalization(self):
        adapter = ShopifyRecharge()
        payload = {"id": "1", "total": "10"}
        env = {"flags": []}
        self.assertEqual(len(adapter.normalize(payload, env)["lines"]), 1)
        env = {"flags": ["split-bundles"]}
        self.assertEqual(len(adapter.normalize(payload, env)["lines"]), 2)
