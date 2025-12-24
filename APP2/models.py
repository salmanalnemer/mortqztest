import uuid

from django.conf import settings
from django.core.validators import MinValueValidator
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


class Department(TimeStampedModel):
    name = models.CharField(_("اسم الإدارة/القسم"), max_length=150, unique=True)
    code = models.CharField(_("الرمز"), max_length=50, unique=True, db_index=True)
    description = models.TextField(_("الوصف"), blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("إدارة/قسم")
        verbose_name_plural = _("الإدارات/الأقسام")

    def __str__(self) -> str:
        return self.name


class Category(TimeStampedModel):
    name = models.CharField(_("اسم التصنيف"), max_length=150, db_index=True)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children",
        verbose_name=_("التصنيف الأب"),
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("تصنيف")
        verbose_name_plural = _("التصنيفات")
        unique_together = ("name", "parent")

    def __str__(self) -> str:
        return self.name


class Asset(TimeStampedModel):
    class Condition(models.TextChoices):
        NEW = "new", _("جديد")
        GOOD = "good", _("جيد")
        FAIR = "fair", _("مقبول")
        POOR = "poor", _("سيء")

    name = models.CharField(_("اسم الأصل/المورد"), max_length=200, db_index=True)
    category = models.ForeignKey(
        Category,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assets",
        verbose_name=_("التصنيف"),
    )
    department = models.ForeignKey(
        Department,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assets",
        verbose_name=_("الإدارة/القسم"),
    )

    serial_number = models.CharField(_("الرقم التسلسلي"), max_length=100, blank=True, db_index=True)
    quantity = models.PositiveIntegerField(_("الكمية"), default=1, validators=[MinValueValidator(1)])
    condition = models.CharField(_("الحالة"), max_length=10, choices=Condition.choices, default=Condition.GOOD)
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("أصل/مورد")
        verbose_name_plural = _("الأصول/الموارد")

    def __str__(self) -> str:
        return self.name


class Attachment(TimeStampedModel):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("الأصل/المورد"),
    )
    title = models.CharField(_("العنوان"), max_length=200, blank=True)
    file = models.FileField(_("الملف"), upload_to="uploads/attachments/%Y/%m/")
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="uploaded_attachments",
        verbose_name=_("تم الرفع بواسطة"),
    )

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("مرفق")
        verbose_name_plural = _("المرفقات")

    def __str__(self) -> str:
        return self.title or f"مرفق {self.id}"


class AssetAssignment(TimeStampedModel):
    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name=_("الأصل/المورد"),
    )
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="asset_assignments",
        verbose_name=_("مُسلّم إلى"),
    )
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="asset_assignments_created",
        verbose_name=_("تم التسليم بواسطة"),
    )
    start_date = models.DateField(_("تاريخ البداية"))
    end_date = models.DateField(_("تاريخ النهاية"), null=True, blank=True)
    note = models.TextField(_("ملاحظة"), blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("تسليم أصل/مورد")
        verbose_name_plural = _("تسليمات الأصول/الموارد")
        indexes = [
            models.Index(fields=["asset", "assigned_to"]),
            models.Index(fields=["start_date", "end_date"]),
        ]

    def __str__(self) -> str:
        return f"{self.asset} -> {self.assigned_to}"
