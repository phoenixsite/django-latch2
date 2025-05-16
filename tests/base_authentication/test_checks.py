"""
Tests for the checks.
"""

# SPDX-License-Identifier: BSD-3-Clause

from io import StringIO

from django.core.management import call_command
from django.core.management.base import SystemCheckError
from django.test import SimpleTestCase, override_settings, modify_settings


class LatchSettingsCheckTest(SimpleTestCase):
    """Tests for the inclusion of required settings."""

    @override_settings(LATCH_APP_ID=None)
    def test_when_latch_app_id_set_to_none(self):
        """
        LATCH_APP_ID not set results in a checking error.
        """

        message = (
            "(django_latch2.E105) 'LATCH_APP_ID' must be included in settings in order to "
            "use the django_latch2 application."
        )
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check")

    @override_settings(LATCH_SECRET_KEY=None)
    def test_when_latch_secret_key_set_to_none(self):
        """
        LATCH_SECRET_KEY not set results in a checking error.
        """

        message = (
            "(django_latch2.E106) 'LATCH_SECRET_KEY' must be included in settings in order to "
            "use the django_latch2 application."
        )
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check")


class DependenciesCheckTest(SimpleTestCase):
    """Tests for dependecy checks."""

    @modify_settings(INSTALLED_APPS={"remove": "django_latch2"})
    def test_app_not_installed(self):
        """
        The checking framework mut not return any error if
        django_latch2 is not included in INSTALLED_APPS.
        """

        stderr = StringIO()
        call_command("check", stderr=stderr)
        message = "django_latch2."
        self.assertNotIn(message, stderr.getvalue())

    @modify_settings(INSTALLED_APPS={"remove": "django.contrib.contenttypes"})
    def test_contenttypes_not_installed(self):
        """
        django.contrib.contenttypes must be included in INSTALLED_APPS.
        """

        message = (
            "(django_latch2.E101) 'django.contrib.contenttypes' must be in "
            "INSTALLED_APPS in order to use the django_latch2 application."
        )
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check")

    # This does not work
    #
    # @modify_settings(INSTALLED_APPS={"remove": "django.contrib.auth"})
    # def test_auth_not_installed(self):
    #    """
    #    django.contrib.auth must be included in INSTALLED_APPS.
    #    """
    #
    #    message = (
    #        "(django_latch2.E102) 'django.contrib.auth' must be in INSTALLED_APPS "
    #        "in order to use the django_latch2 application."
    #    )
    #    with self.assertRaises(KeyError):
    #    #with self.assertRaisesMessage(SystemCheckError, message):
    #        call_command("check")
    #

    @modify_settings(
        MIDDLEWARE={"remove": "django.contrib.auth.middleware.AuthenticationMiddleware"}
    )
    def test_auth_middleware_not_installed(self):
        """
        django.contrib.auth.middleware.AuthenticationMiddleware
        must be included in MIDDLEWARE.
        """

        message = (
            "(django_latch2.E103) 'django.contrib.auth.middleware.AuthenticationMiddleware' must "
            "be in MIDDLEWARE in order to use the django_latch2 application."
        )
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check")

    @override_settings(
        AUTHENTICATION_BACKENDS=["django.contrib.auth.backends.ModelBackend"]
    )
    def test_no_latch_backend(self):
        """
        A subclass of LatchModelBackendMixin must be included in AUTHENTICATION_BACKEND.
        """

        message = (
            "(django_latch2.E104) 'django_latch2.backends.LatchModelBackendMixin' must "
            "be a subclass of some in AUTHENTICATION_BACKENDS in order to use the "
            "django_latch2 application."
        )
        with self.assertRaisesMessage(SystemCheckError, message):
            call_command("check")
