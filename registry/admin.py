from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.forms import IntegerField
from django.utils.translation import gettext_lazy as _
from unfold.admin import TabularInline, ModelAdmin
from unfold.forms import ActionForm
from unfold.widgets import UnfoldAdminIntegerFieldWidget

from registry.models import (
    Service,
    ServiceURL,
    ServiceInfo,
    ServiceInfoType,
    ServiceInfoPoint,
    ServiceInfoCategory,
)


class UnfoldMovePageActionForm(ActionForm):
    step = IntegerField(
        required=False,
        initial=1,
        # from unfold.widgets import UnfoldAdminIntegerFieldWidget
        widget=UnfoldAdminIntegerFieldWidget(attrs={"id": "changelist-form-step"}),
        label=False,
    )
    page = IntegerField(
        required=False,
        widget=UnfoldAdminIntegerFieldWidget(attrs={"id": "changelist-form-page"}),
        label=False,
    )


# Replace action_form in extended class
class SortableMixin(SortableAdminMixin):
    action_form = UnfoldMovePageActionForm


class ServiceURLInline(TabularInline):
    model = ServiceURL
    extra = 1


class ServiceInfoInline(TabularInline):
    model = ServiceInfo
    extra = 1


class ServiceInfoPointInline(TabularInline):
    model = ServiceInfoPoint
    extra = 1


@admin.register(Service)
class ServiceAdmin(ModelAdmin):
    list_display = (
        "name",
        "website",
        "rating",
        "icon_class",
        "has_image",
        "updated_at",
        "is_active",
    )
    search_fields = ("name", "website")
    ordering = ("name",)
    list_filter = ("is_active",)
    inlines = [ServiceURLInline, ServiceInfoInline]
    prepopulated_fields = {"slug": ("name",)}
    actions = ["make_active", "make_inactive"]

    @admin.display(boolean=True, description=_("Has Image"))
    def has_image(self, obj):
        return bool(obj.image)

    @admin.action(description=_("Make selected Services active"))
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected Services are now active."), "success")

    @admin.action(description=_("Make selected Services inactive"))
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected Services are now inactive."), "success")


@admin.register(ServiceURL)
class ServiceURLAdmin(ModelAdmin):
    list_display = ("service", "url_type", "url", "created_at", "updated_at")
    search_fields = ("service__name", "url_type", "url")
    list_filter = ("url_type",)
    ordering = ("service", "url_type")


@admin.register(ServiceInfoType)
class ServiceInfoTypeAdmin(ModelAdmin):
    list_display = ("name", "icon_class", "updated_at")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(ServiceInfoCategory)
class ServiceInfoCategoryAdmin(SortableMixin, ModelAdmin):
    list_display = ("name", "created_at", "updated_at", "order")
    search_fields = ("name",)


@admin.register(ServiceInfo)
class ServiceInfoAdmin(ModelAdmin):
    list_display = ("type", "description", "created_at", "updated_at")
    search_fields = ("description", "type__name")
    list_filter = ("type",)
    ordering = ("type",)
    inlines = [ServiceInfoPointInline]


@admin.register(ServiceInfoPoint)
class ServiceInfoPointAdmin(ModelAdmin):
    list_display = ("service_info", "text", "created_at", "updated_at")
    search_fields = ("service_info__description", "text")
    list_filter = ("service_info",)
    ordering = ("service_info",)
