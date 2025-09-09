from sheetmusic.apps.integrations.registry import register, resolve
from sheetmusic.apps.integrations.base import BaseAdapter

from django.test import SimpleTestCase
from sheetmusic.apps.integrations.registry import register, resolve
from sheetmusic.apps.integrations.base import BaseAdapter


@register("provider.v1.kind", "provider.v1.*")
class Broad(BaseAdapter):
    def identify_external_id(self, payload):
        return "1"

    def normalize(self, payload, envelope):
        return {}


@register("provider.v1.kind.special")
class Specific(BaseAdapter):
    def identify_external_id(self, payload):
        return "1"

    def normalize(self, payload, envelope):
        return {}


class RegistryTests(SimpleTestCase):
    def test_resolve_most_specific(self):
        cls = resolve("provider.v1.kind.special")
        self.assertIs(cls, Specific)
        cls = resolve("provider.v1.kind.other")
        self.assertIs(cls, Broad)
