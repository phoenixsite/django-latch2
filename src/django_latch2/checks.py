"""
Checks for django-latch2.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.apps import apps
from django.core import checks
from django.utils.module_loading import import_string
from django.conf import settings


def _issubclass(cls, classinfo):
    """
    issubclass() variant that doesn't raise an exception if cls isn't a
    class.

    Copied from django.contrib.admin.checks.
    """
    try:
        return issubclass(cls, classinfo)
    except TypeError:  # pragma: no cover
        return False


def _contains_subclass(class_path, candidate_paths):
    """
    Return whether or not a dotted class path (or a subclass of that class) is
    found in a list of candidate paths.

    Copied from django.contrib.admin.checks.
    """

    cls = import_string(class_path)
    for path in candidate_paths:
        try:
            candidate_cls = import_string(path)
        except ImportError:  # pragma: no cover
            continue
        if _issubclass(candidate_cls, cls):
            return True
    return False  # pragma: no cover


def check_dependencies(app_configs, **kwargs):  # pylint: disable=unused-argument
    """
    Check that the django-latch2's dependencies are installed in the project.
    """

    if not apps.is_installed("django_latch2"):
        return []

    errors = []
    app_dependencies = (
        ("django.contrib.contenttypes", 101),
        ("django.contrib.auth", 102),
    )

    # Check for installed apps
    for app_name, error_code in app_dependencies:
        if not apps.is_installed(app_name):
            errors.append(
                checks.Error(
                    f"'{app_name}' must be in INSTALLED_APPS in order to use the "
                    "django_latch2 application.",
                    id=f"django_latch2.E{error_code}",
                )
            )

    # Check for the authentication middleware
    if not _contains_subclass(
        "django.contrib.auth.middleware.AuthenticationMiddleware", settings.MIDDLEWARE
    ):
        errors.append(
            checks.Error(
                "'django.contrib.auth.middleware.AuthenticationMiddleware' must "
                "be in MIDDLEWARE in order to use the django_latch2 application.",
                id="django_latch2.E103",
            )
        )

    # Check for the authentication backend
    if not _contains_subclass(
        "django_latch2.backends.LatchModelBackendMixin",
        settings.AUTHENTICATION_BACKENDS,
    ):
        errors.append(
            checks.Error(
                "'django_latch2.backends.LatchModelBackendMixin' must be a subclass of "
                "some in AUTHENTICATION_BACKENDS in order to use the "
                "django_latch2 application.",
                id="django_latch2.E104",
            )
        )
    return errors


def check_settings(app_configs, **kwargs):  # pylint: disable=unused-argument
    """
    Check that the Latch's application id and secret key settings are set.
    """

    errors = []
    req_settings = (
        ("LATCH_APP_ID", 105),
        ("LATCH_SECRET_KEY", 106),
    )

    for setting_name, error_code in req_settings:
        if (
            getattr(settings, setting_name, None) is None
            or getattr(settings, setting_name, None) == ""
        ):
            errors.append(
                checks.Error(
                    f"'{setting_name}' must be included in settings in order to "
                    "use the django_latch2 application.",
                    id=f"django_latch2.E{error_code}",
                )
            )
    return errors
