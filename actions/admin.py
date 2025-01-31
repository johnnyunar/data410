from django.contrib import admin
from unfold.admin import ModelAdmin

from actions.models import Action

from django.utils.translation import gettext_lazy as _


@admin.register(Action)
class ServiceAdmin(ModelAdmin):
    list_display = ("name", "service", "handler", "is_active")
    search_fields = ("name", "service__name", "handler")
    list_filter = ("is_active",)
    actions = ["make_active", "make_inactive"]
    readonly_fields = ("created_at", "updated_at", "order")

    @admin.action(description=_("Make selected Services active"))
    def make_active(self, request, queryset):
        queryset.update(is_active=True)
        self.message_user(request, _("Selected Services are now active."), "success")

    @admin.action(description=_("Make selected Services inactive"))
    def make_inactive(self, request, queryset):
        queryset.update(is_active=False)
        self.message_user(request, _("Selected Services are now inactive."), "success")
