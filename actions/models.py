from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import BaseModelSortable


class Action(BaseModelSortable):
    service = models.ForeignKey(
        "registry.Service",
        on_delete=models.CASCADE,
        related_name="actions",
        help_text=_("The service this action is associated with."),
    )
    name = models.CharField(max_length=255, help_text=_("Name of the action."))
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Detailed description of what this action does."),
    )

    handler = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text=_(
            "Path to a custom handler for this action. Example: actions.handlers.nice_service.delete_comments"
        ),
    )

    def __str__(self):
        return f"{self.service.name}: {self.name}"

    class Meta:
        verbose_name = _("Action")
        verbose_name_plural = _("Actions")
