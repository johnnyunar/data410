from django.db import models
from django.urls import reverse

from core.models import BaseModel

from django.utils.translation import gettext_lazy as _


class ServiceInfoType(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Name of the service info type, e.g., What to be aware of, How to delete data.",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service Info Type")
        verbose_name_plural = _("Service Info Types")


class ServiceInfo(BaseModel):
    description = models.TextField(
        blank=True, null=True, help_text="Description of the service."
    )
    type = models.ForeignKey(
        ServiceInfoType,
        on_delete=models.CASCADE,
        related_name="service_infos",
        help_text=_("Type of service info."),
    )
    service = models.ForeignKey(
        "Service",
        on_delete=models.CASCADE,
        related_name="service_infos",
        help_text=_("The third-party service associated with this info."),
    )

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = _("Service Info")
        verbose_name_plural = _("Service Infos")


class ServiceInfoPoint(BaseModel):
    # Related Service Info
    service_info = models.ForeignKey(
        ServiceInfo,
        on_delete=models.CASCADE,
        related_name="points",
        help_text=_("The service info associated with this point."),
    )
    text = models.CharField(
        max_length=255,
        help_text=_("A point of information about the service."),
    )

    def __str__(self):
        return self.service_info

    class Meta:
        verbose_name = _("Service Info Point")
        verbose_name_plural = _("Service Info Points")


class Service(BaseModel):
    # Basic Info
    name = models.CharField(
        max_length=255, unique=True, help_text="Name of the third-party service."
    )
    website = models.URLField(
        blank=True, null=True, help_text="Official website of the service."
    )
    image = models.ImageField(
        blank=True,
        null=True,
        help_text=_("Logo or image representing the service."),
    )

    def get_absolute_url(self):
        return reverse("service-detail", kwargs={"uuid": self.uuid})

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")


class ServiceURL(BaseModel):
    # Related Service
    service = models.ForeignKey(
        Service,
        on_delete=models.CASCADE,
        related_name="urls",
        help_text="The third-party service associated with this URL.",
    )
    url_type = models.CharField(
        max_length=100,
        help_text=_(
            "Type or purpose of the URL (e.g., API docs, support page, privacy policy, data removal page)."
        ),
    )
    url = models.URLField()

    def __str__(self):
        return f"{self.service.name} - {self.url_type}"

    class Meta:
        verbose_name = _("Service URL")
        verbose_name_plural = _("Service URLs")
