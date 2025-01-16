from django.db import models

from django.utils.translation import gettext_lazy as _


class RequestLog(models.Model):
    path = models.CharField(
        _("Path"), max_length=255, unique=True, help_text=_("The requested URL path.")
    )
    user_count = models.PositiveIntegerField(
        _("User Count"), default=0, help_text=_("Number of requests by users.")
    )
    bot_count = models.PositiveIntegerField(
        _("Bot Count"), default=0, help_text=_("Number of requests by bots.")
    )

    class Meta:
        verbose_name = _("Request Log")
        verbose_name_plural = _("Request Logs")
        ordering = ["path"]

    def __str__(self):
        return f"{self.path}"
