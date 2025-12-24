from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class App1Config(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "APP1"
    verbose_name = _("التطبيق الأول")
