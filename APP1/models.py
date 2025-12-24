import uuid

from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator
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


phone_validator = RegexValidator(
    regex=r"^\+?\d{8,15}$",
    message=_("أدخل رقم جوال صحيح (8-15 رقم) ويمكن أن يبدأ بـ +."),
)


class Profile(TimeStampedModel):
    class Gender(models.TextChoices):
        MALE = "male", _("ذكر")
        FEMALE = "female", _("أنثى")
        OTHER = "other", _("أخرى")

    class Role(models.TextChoices):
        ADMIN = "admin", _("مدير نظام")
        MANAGER = "manager", _("مدير")
        STAFF = "staff", _("موظف")
        USER = "user", _("مستخدم")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("المستخدم"),
    )
    full_name = models.CharField(_("الاسم الكامل"), max_length=200, blank=True)
    phone = models.CharField(_("رقم الجوال"), max_length=20, blank=True, validators=[phone_validator], db_index=True)
    national_id = models.CharField(
        _("رقم الهوية/المعرف"),
        max_length=20,
        blank=True,
        validators=[MinLengthValidator(8)],
        help_text=_("حقل اختياري (يفضّل تشفيره في بيئة الإنتاج)."),
    )
    role = models.CharField(_("الدور"), max_length=20, choices=Role.choices, default=Role.USER, db_index=True)
    gender = models.CharField(_("الجنس"), max_length=10, choices=Gender.choices, blank=True)
    birth_date = models.DateField(_("تاريخ الميلاد"), null=True, blank=True)

    preferred_language = models.CharField(_("اللغة المفضلة"), max_length=10, default="ar", db_index=True)
    timezone = models.CharField(_("المنطقة الزمنية"), max_length=64, default="Asia/Riyadh")
    notes = models.TextField(_("ملاحظات"), blank=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("الملف الشخصي")
        verbose_name_plural = _("الملفات الشخصية")

    def __str__(self) -> str:
        return self.full_name or getattr(self.user, "username", "ملف شخصي")


class Address(TimeStampedModel):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="addresses",
        verbose_name=_("الملف الشخصي"),
    )
    label = models.CharField(_("التسمية"), max_length=50, blank=True, help_text=_("مثال: المنزل، العمل"))
    city = models.CharField(_("المدينة"), max_length=100)
    district = models.CharField(_("الحي"), max_length=100, blank=True)
    street = models.CharField(_("الشارع"), max_length=200, blank=True)
    postal_code = models.CharField(_("الرمز البريدي"), max_length=20, blank=True)
    is_default = models.BooleanField(_("افتراضي"), default=False, db_index=True)

    class Meta(TimeStampedModel.Meta):
        verbose_name = _("العنوان")
        verbose_name_plural = _("العناوين")
        indexes = [
            models.Index(fields=["profile", "is_default"]),
        ]

    def __str__(self) -> str:
        return f"{self.city} - {self.label or 'عنوان'}"
