# app2/admin.py
from django.contrib import admin

from .models import Department, Category, Asset, Attachment, AssetAssignment


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "is_active", "created_at")
    search_fields = ("name", "code")
    list_filter = ("is_active",)
    ordering = ("name",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "parent", "is_active", "created_at")
    search_fields = ("name",)
    list_filter = ("is_active",)
    ordering = ("name",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "category", "serial_number", "quantity", "condition", "is_active")
    list_filter = ("condition", "department", "category", "is_active")
    search_fields = ("name", "serial_number")
    ordering = ("name",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("asset", "title", "uploaded_by", "created_at")
    search_fields = ("title", "asset__name", "uploaded_by__username", "uploaded_by__email")
    list_filter = ("created_at",)
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(AssetAssignment)
class AssetAssignmentAdmin(admin.ModelAdmin):
    list_display = ("asset", "assigned_to", "start_date", "end_date", "is_active", "created_at")
    list_filter = ("start_date", "end_date", "is_active")
    search_fields = ("asset__name", "assigned_to__username", "assigned_to__email")
    ordering = ("-start_date",)
    readonly_fields = ("id", "created_at", "updated_at")
