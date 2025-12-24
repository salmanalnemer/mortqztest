# app3/admin.py
from django.contrib import admin

from .models import Project, Task, Comment, ActivityLog


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("name", "owner", "is_active", "created_at")
    search_fields = ("name", "owner__username", "owner__email")
    list_filter = ("is_active",)
    ordering = ("name",)
    readonly_fields = ("id", "created_at", "updated_at")
    filter_horizontal = ("members",)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("title", "project", "status", "priority", "assigned_to", "due_date", "progress", "is_active")
    list_filter = ("status", "priority", "project", "is_active")
    search_fields = ("title", "project__name", "assigned_to__username", "assigned_to__email")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("task", "author", "created_at", "is_active")
    list_filter = ("created_at", "is_active")
    search_fields = ("task__title", "author__username", "author__email", "body")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    list_display = ("action", "actor", "message", "created_at")
    list_filter = ("action", "created_at")
    search_fields = ("message", "actor__username", "actor__email")
    ordering = ("-created_at",)
    readonly_fields = ("id", "created_at", "updated_at")
