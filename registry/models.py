from functools import partial

from django.db import models
from django.urls import reverse
from django_prose_editor.sanitized import SanitizedProseEditorField

from core.models import BaseModel, BaseModelSortable

from django.utils.translation import gettext_lazy as _

from core.utils import generate_random_filename
from registry.icons import FAB_ICONS


class ServiceInfoType(BaseModel):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_(
            "Name of the service info type, e.g., What to be aware of, How to delete data."
        ),
    )
    icon_class = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_(
            "FontAwesome class for an icon representing this type. E.g., fas fa-lock."
        ),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service Info Type")
        verbose_name_plural = _("Service Info Types")


class ServiceInfoCategory(BaseModelSortable):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_("Name of the service info category, e.g., Privacy, Security, AI."),
    )

    def __str__(self):
        return self.name

    class Meta(BaseModelSortable.Meta):
        verbose_name = _("Service Info Category")
        verbose_name_plural = _("Service Info Categories")


class ServiceInfo(BaseModel):
    description = SanitizedProseEditorField(
        blank=True, null=True, help_text="Description of the service."
    )
    type = models.ForeignKey(
        ServiceInfoType,
        on_delete=models.CASCADE,
        related_name="service_infos",
        help_text=_("Type of service info."),
    )
    category = models.ForeignKey(
        ServiceInfoCategory,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="service_infos",
        help_text=_("Category of service info."),
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
        return self.text

    class Meta:
        verbose_name = _("Service Info Point")
        verbose_name_plural = _("Service Info Points")


class Service(BaseModel):
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
        upload_to=partial(generate_random_filename, subdir="services/images/"),
    )

    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        blank=True,
        null=True,
        help_text=_("Average rating of the service."),
    )

    slug = models.SlugField(
        max_length=255,
        unique=True,
        help_text=_("Unique URL path to access this service."),
    )

    icon_class = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text=_(
            "FontAwesome class for an icon representing this Service. E.g., fab fa-google."
        ),
    )

    def get_absolute_url(self):
        return reverse("service-detail", kwargs={"slug": self.slug})

    def save(self, *args, **kwargs):
        # Set a default icon_class if not explicitly provided
        if not self.icon_class:
            formatted_name = self.name.lower().replace(" ", "-")
            if formatted_name in FAB_ICONS:
                self.icon_class = f"fab fa-{formatted_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Service")
        verbose_name_plural = _("Services")
        ordering = ["name"]


class ServiceURL(BaseModel):
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
