from typing import Dict, Any


class BaseHealthCheck:
    """
    A base class for defining health checks.
    Subclasses should implement the `check` method to perform specific health checks.
    """

    name: str = "base"

    def check(self, **kwargs) -> Dict[str, Any]:
        """
        Perform the health check and return the status and additional details.
        Must return a dictionary with at least `status: "ok" | "error"`.
        """
        raise NotImplementedError("Subclasses must implement the `check` method.")

    @property
    def verbose_name(self) -> str:
        """
        Return a human-readable name for the health check.
        """
        # Convert the name to title case
        return self.name.replace("_", " ").title()
