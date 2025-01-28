from django.utils.timezone import now
from django.conf import settings
from django.core.cache import cache, caches
from django.core.cache.backends.base import InvalidCacheBackendError
from django.views.generic import TemplateView
from health.registry import HealthCheckRegistry


class HealthCheckDashboardView(TemplateView):
    """
    TemplateView to render the health check results in a user-friendly HTML template.
    """

    template_name = "health/dashboard.html"
    CACHE_KEY = "healthcheck_dashboard"
    CACHE_TIMEOUT = 30 * 60  # 30 minutes

    def is_cache_available(self) -> bool:
        """
        Check if the cache backend is available and configured.
        """
        try:
            caches["default"].get(self.CACHE_KEY)
            return True
        except:
            return False

    def generate_healthcheck_results(self, request) -> dict:
        """
        Generate fresh health check results.
        """
        healthchecks = HealthCheckRegistry.get_registered_healthchecks()
        results = {check.verbose_name: check.check() for check in healthchecks}
        last_update = now()
        return {"results": results, "last_update": last_update}

    def get_cached_healthcheck_results(self) -> dict:
        """
        Retrieve health check results from the cache.
        """
        cached_data = cache.get(self.CACHE_KEY)
        return cached_data if cached_data else None

    def cache_healthcheck_results(self, data: dict) -> None:
        """
        Cache health check results.
        """
        cache.set(self.CACHE_KEY, data, self.CACHE_TIMEOUT)

    def get_context_data(self, **kwargs):
        """
        Prepare the context data for rendering the dashboard.
        """
        context = super().get_context_data(**kwargs)
        request = self.request

        if settings.DEBUG or not self.is_cache_available():
            # Generate and use live health check results
            data = self.generate_healthcheck_results(request)
        else:
            # Try to get cached results, fallback to generating fresh results
            cached_data = self.get_cached_healthcheck_results()
            if cached_data:
                data = cached_data
            else:
                data = self.generate_healthcheck_results(request)
                self.cache_healthcheck_results(data)

        # Format the last update timestamp and add results to the context
        context["results"] = data["results"]
        context["last_update"] = data["last_update"].strftime("%Y-%m-%d %H:%M:%S %Z")
        return context
