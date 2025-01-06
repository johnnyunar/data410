from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin
from django.forms import IntegerField
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
    list_display = ("name", "website", "image", "created_at", "updated_at")
    search_fields = ("name", "website")
    ordering = ("name",)
    inlines = [ServiceURLInline, ServiceInfoInline]


@admin.register(ServiceURL)
class ServiceURLAdmin(ModelAdmin):
    list_display = ("service", "url_type", "url", "created_at", "updated_at")
    search_fields = ("service__name", "url_type", "url")
    list_filter = ("url_type",)
    ordering = ("service", "url_type")


@admin.register(ServiceInfoType)
class ServiceInfoTypeAdmin(ModelAdmin):
    list_display = ("name", "created_at", "updated_at")
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
