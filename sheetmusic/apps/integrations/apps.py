from django.apps import AppConfig
from importlib import import_module
import pkgutil


class IntegrationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "sheetmusic.apps.integrations"

    def ready(self):
        """Auto-import adapter modules so registry is populated."""
        package_name = f"{self.name}.adapters"
        package = import_module(package_name)
        for _, modname, _ in pkgutil.iter_modules(package.__path__, package_name + "."):
            import_module(modname)
