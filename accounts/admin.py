from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "first_name", "last_name", "phone", "is_staff")
    search_fields = ("username", "email", "first_name", "last_name", "phone")

    fieldsets = UserAdmin.fieldsets + (("Додатково", {"fields": ("phone",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Додатково", {"fields": ("email", "phone")}),
    )
