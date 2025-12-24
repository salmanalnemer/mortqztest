# app1/admin.py
from django.contrib import admin

from .models import Profile, Address


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "full_name", "phone", "role", "is_active", "created_at")
    list_filter = ("role", "is_active", "preferred_language")
    search_fields = ("full_name", "phone", "user__username", "user__email")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("user", "full_name", "role", "is_active")}),
        ("Contact", {"fields": ("phone", "national_id")}),
        ("Preferences", {"fields": ("preferred_language", "timezone")}),
        ("Other", {"fields": ("gender", "birth_date", "notes")}),
        ("Meta", {"fields": ("id", "created_at", "updated_at")}),
    )


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("profile", "label", "city", "district", "is_default", "is_active", "created_at")
    list_filter = ("city", "is_default", "is_active")
    search_fields = ("profile__full_name", "city", "district", "street", "postal_code")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")
