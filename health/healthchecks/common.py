import requests
from django.core.cache import cache
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import connections
from django.urls import reverse

from health.decorators import register_healthcheck
from health.healthchecks.base import BaseHealthCheck


@register_healthcheck
class CacheHealthCheck(BaseHealthCheck):
    name = "cache"

    def check(self, **kwargs) -> dict:
        try:
            cache.set("healthcheck", "ok", timeout=1)
            result = cache.get("healthcheck")
            if result == "ok":
                return {"status": "ok"}
            return {"status": "error", "details": "Cache misconfiguration."}
        except Exception as e:
            return {"status": "error", "details": str(e)}


@register_healthcheck
class DatabaseHealthCheck(BaseHealthCheck):
    name = "database"

    def check(self, **kwargs) -> dict:
        try:
            with connections["default"].cursor() as cursor:
                cursor.execute("SELECT 1")
            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "details": str(e)}


@register_healthcheck
class FileStorageHealthCheck(BaseHealthCheck):
    name = "storage"

    def check(self, **kwargs) -> dict:
        try:
            # Path for the healthcheck test file
            test_file = "healthcheck/healthcheck_test_file.txt"
            content = b"healthcheck"

            # Ensure the "healthcheck" directory exists (for local file systems)
            if not default_storage.exists("healthcheck/"):
                default_storage.save(
                    "healthcheck/.keep", ContentFile(b"")
                )  # Create a placeholder file

            # Write the test file
            with default_storage.open(test_file, "wb") as f:
                f.write(content)

            # Verify the file exists
            if not default_storage.exists(test_file):
                return {"status": "error", "details": "File not found after creation."}

            # Clean up: Delete the test file
            default_storage.delete(test_file)

            return {"status": "ok"}
        except Exception as e:
            return {"status": "error", "details": str(e)}
