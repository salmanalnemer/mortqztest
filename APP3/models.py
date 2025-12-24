import uuid

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    id = models.UUIDField(_("المعرف"), primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(_("نشط"), default=True, db_index=True)
    created_at = models.DateTimeField(_("تاريخ الإنشاء"), auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(_("تاريخ التحديث"), auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


class Project(TimeStampedModel):
    name = models.CharField(_("اسم المشروع"), max_length=200, db_index=True)
    description = models.TextField(_("وصف المشروع"), blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="owned_projects",
        verbose_name=_("المالك"),
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        blank=True,
        related_name="projects",
        verbose_name=_("الأعضاء"),
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("مشروع")
        verbose_name_plural = _("المشاريع")

    def __str__(self) -> str:
        return self.name


class Task(TimeStampedModel):
    class Status(models.TextChoices):
        TODO = "todo", _("قيد الانتظار")
        IN_PROGRESS = "in_progress", _("قيد التنفيذ")
        DONE = "done", _("مكتملة")
        CANCELED = "canceled", _("ملغاة")

    class Priority(models.IntegerChoices):
        LOW = 1, _("منخفضة")
        MEDIUM = 2, _("متوسطة")
        HIGH = 3, _("عالية")
        URGENT = 4, _("عاجلة")

    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="tasks", verbose_name=_("المشروع"))
    title = models.CharField(_("عنوان المهمة"), max_length=200, db_index=True)
    description = models.TextField(_("وصف المهمة"), blank=True)
    status = models.CharField(_("الحالة"), max_length=20, choices=Status.choices, default=Status.TODO, db_index=True)
    priority = models.IntegerField(_("الأولوية"), choices=Priority.choices, default=Priority.MEDIUM, db_index=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks_created",
        verbose_name=_("أُنشئت بواسطة"),
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="tasks_assigned",
        verbose_name=_("مُسندة إلى"),
    )

    due_date = models.DateField(_("تاريخ الاستحقاق"), null=True, blank=True)
    progress = models.PositiveSmallIntegerField(
        _("نسبة الإنجاز"),
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text=_("من 0 إلى 100"),
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("مهمة")
        verbose_name_plural = _("المهام")
        indexes = [
            models.Index(fields=["project", "status"]),
            models.Index(fields=["assigned_to", "status"]),
        ]

    def __str__(self) -> str:
        return self.title


class Comment(TimeStampedModel):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments", verbose_name=_("المهمة"))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="task_comments",
        verbose_name=_("الكاتب"),
    )
    body = models.TextField(_("نص التعليق"))

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("تعليق")
        verbose_name_plural = _("التعليقات")

    def __str__(self) -> str:
        return f"تعليق {self.id}"


class ActivityLog(TimeStampedModel):
    class Action(models.TextChoices):
        CREATE = "create", _("إنشاء")
        UPDATE = "update", _("تحديث")
        DELETE = "delete", _("حذف")
        LOGIN = "login", _("تسجيل دخول")
        OTHER = "other", _("أخرى")

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="activity_logs",
        verbose_name=_("المنفّذ"),
    )
    action = models.CharField(_("الحدث"), max_length=20, choices=Action.choices, default=Action.OTHER, db_index=True)
    message = models.CharField(_("الوصف"), max_length=500)
    metadata = models.JSONField(_("بيانات إضافية"), default=dict, blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("سجل النشاط")
        verbose_name_plural = _("سجلات النشاط")

    def __str__(self) -> str:
        return f"{self.action}: {self.message[:40]}"
