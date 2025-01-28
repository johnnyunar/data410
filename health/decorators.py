from health.registry import HealthCheckRegistry


def register_healthcheck(healthcheck_class):
    """
    Decorator to register health checks automatically.
    """
    HealthCheckRegistry.register(healthcheck_class)
    return healthcheck_class
