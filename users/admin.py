from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from unfold.admin import ModelAdmin

from users.models import DataUser


@admin.register(DataUser)
class DataUserAdmin(UserAdmin, ModelAdmin):
    model = DataUser
    list_display = ("email", "username", "first_name", "last_name", "is_staff")
    add_fieldsets = UserAdmin.add_fieldsets + ((None, {"fields": ("email",)}),)
    search_fields = ("email", "username")
