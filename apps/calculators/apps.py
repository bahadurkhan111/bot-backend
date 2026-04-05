from django.apps import AppConfig


class CalculatorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.calculators'
    
    def ready(self):
        """Import calculator registry to ensure calculators are registered."""
        from . import registry
