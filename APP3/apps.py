# app3/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class App3Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "APP3"
    verbose_name = _("التطبيق الثالث")
