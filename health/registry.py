from typing import List, Type

from health.healthchecks.base import BaseHealthCheck


class HealthCheckRegistry:
    """
    Registry to manage and store health checks for the entire project.
    """

    _registry: List[Type[BaseHealthCheck]] = []

    @classmethod
    def register(cls, healthcheck_class: Type[BaseHealthCheck]):
        """
        Register a health check class.
        """
        if not issubclass(healthcheck_class, BaseHealthCheck):
            raise ValueError(
                f"{healthcheck_class.__name__} must inherit from BaseHealthCheck."
            )
        cls._registry.append(healthcheck_class)

    @classmethod
    def get_registered_healthchecks(cls) -> List[BaseHealthCheck]:
        """
        Get a list of instantiated health checks from the registry.
        """
        return [healthcheck() for healthcheck in cls._registry]
