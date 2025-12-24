# app1/models.py
import uuid

from django.conf import settings
from django.core.validators import RegexValidator, MinLengthValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """Abstract base: UUID + timestamps + active flag."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)


phone_validator = RegexValidator(
    regex=r"^\+?\d{8,15}$",
    message=_("Enter a valid phone number (8-15 digits), optionally starting with +."),
)


class Profile(TimeStampedModel):
    """User profile extension (safe to keep AUTH_USER_MODEL default)."""
    class Gender(models.TextChoices):
        MALE = "male", _("Male")
        FEMALE = "female", _("Female")
        OTHER = "other", _("Other")

    class Role(models.TextChoices):
        ADMIN = "admin", _("Admin")
        MANAGER = "manager", _("Manager")
        STAFF = "staff", _("Staff")
        USER = "user", _("User")

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    full_name = models.CharField(max_length=200, blank=True)
    phone = models.CharField(max_length=20, blank=True, validators=[phone_validator], db_index=True)
    national_id = models.CharField(
        max_length=20,
        blank=True,
        validators=[MinLengthValidator(8)],
        help_text=_("Optional identifier (store carefully in production)."),
    )
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER, db_index=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    birth_date = models.DateField(null=True, blank=True)

    # optional preferences
    preferred_language = models.CharField(max_length=10, default="ar", db_index=True)
    timezone = models.CharField(max_length=64, default="Asia/Riyadh")
    notes = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.full_name or getattr(self.user, "username", "Profile")


class Address(TimeStampedModel):
    """Optional multiple addresses for a profile."""
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=50, blank=True, help_text=_("e.g., Home, Work"))
    city = models.CharField(max_length=100)
    district = models.CharField(max_length=100, blank=True)
    street = models.CharField(max_length=200, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    is_default = models.BooleanField(default=False, db_index=True)

    class Meta(TimeStampedModel.Meta):
        indexes = [
            models.Index(fields=["profile", "is_default"]),
        ]

    def __str__(self) -> str:
        return f"{self.city} - {self.label or 'Address'}"
