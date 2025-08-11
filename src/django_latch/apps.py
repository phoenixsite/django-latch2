"""
App configuration module of django-latch.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.apps import AppConfig
from django.core import checks
from django.utils.translation import gettext_lazy as _

from .checks import check_dependencies, check_settings


class DjangoLatch2Config(AppConfig):
    """
    Application and configuration of django-latch.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "django_latch"
    verbose_name = _("Latch for Django")

    def ready(self):
        """Run the checks."""
        checks.register(check_dependencies)
        checks.register(check_settings)
