from django.contrib import admin
from unfold.admin import ModelAdmin

from .models import RequestLog


@admin.register(RequestLog)
class RequestLogAdmin(ModelAdmin):
    list_display = ("path", "user_count", "bot_count")
    search_fields = ("path",)
    ordering = ("-user_count", "-bot_count")
