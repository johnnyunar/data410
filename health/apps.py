from django.apps import AppConfig


class HealthConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "health"

    def ready(self):
        # Import the module containing healthchecks to trigger registration
        import health.healthchecks.common  # noqa
