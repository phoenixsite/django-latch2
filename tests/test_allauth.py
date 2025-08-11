"""
Tests for using ``django-latch``along with
`django-allauth <https://allauth.org/>`_.
"""

from http import HTTPStatus
from unittest.mock import patch, Mock

from django.test import override_settings, modify_settings
from django.conf import settings

from .test_workflow import (
    AnonymousUserTests as BaseAnonymousUserTests,
    PairedUserTests as BasePairedUserTests,
    UnpairedUserTests as BaseUnpairedUserTests,
    mock_status_true,
    reverse,
)
from .test_backend import LatchBackendTestCase as BaseLatchBackendTestCase


@override_settings(
    AUTHENTICATION_BACKENDS=["tests.backends.LatchAuthenticationAllauthBackend"],
    ROOT_URLCONF="tests.urls_allauth",
)
@modify_settings(
    MIDDLEWARE={"append": "allauth.account.middleware.AccountMiddleware"},
    INSTALLED_APPS={"append": ["allauth", "allauth.account"]},
)
class AnonymousUserTests(BaseAnonymousUserTests):
    """
    Test pairing and unpairing with an anonymous user using the
    ``django-allauth`` authentication backend.
    """

    def test_acccess_allauth_views(self):
        """
        An anonymous user should be able to access to all the
        ``django-allauth`` views that don't require log in.
        """

        viewnames = [
            "account_login",
            "account_inactive",
            "account_signup",
            "account_email_verification_sent",
            "account_reset_password",
        ]

        for viewname in viewnames:
            with self.subTest(viewname=viewname):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(resp.status_code, HTTPStatus.OK)

        viewname = "account_confirm_email"
        with self.subTest(viewname=viewname):
            resp = self.client.get(reverse(viewname, args="1"))
            self.assertEqual(resp.status_code, HTTPStatus.OK)

        viewname = "account_confirm_login_code"
        with self.subTest(viewname=viewname):
            resp = self.client.get(reverse(viewname))
            self.assertRedirects(resp, settings.LOGIN_URL)

    def test_forbidden_allauth_views(self):
        """
        An anonymous user shouldn't be able to access to all the
        ``django-allauth`` views that require log in.
        """

        viewnames = [
            "account_reauthenticate",
            "account_email",
            "account_change_password",
            "account_set_password",
        ]

        for viewname in viewnames:
            with self.subTest(viewname=viewname):
                resp = self.client.get(reverse(viewname))
                self.assertRedirects(
                    resp, f"{settings.LOGIN_URL}?next={reverse(viewname)}"
                )

        viewname = "account_confirm_login_code"
        with self.subTest(viewname=viewname):
            resp = self.client.get(reverse(viewname))
            self.assertRedirects(resp, settings.LOGIN_URL)

        viewname = "account_logout"
        with self.subTest(viewname=viewname):
            resp = self.client.get(reverse(viewname))
            self.assertRedirects(resp, "/")


@override_settings(
    AUTHENTICATION_BACKENDS=["tests.backends.LatchAuthenticationAllauthBackend"],
    ROOT_URLCONF="tests.urls_allauth",
)
@modify_settings(
    MIDDLEWARE={"append": "allauth.account.middleware.AccountMiddleware"},
    INSTALLED_APPS={"append": ["allauth", "allauth.account"]},
)
class UnpairedUserTests(BaseUnpairedUserTests):
    """
    Tests for an unpaired authenticated user using the ``django-allauth``
    authentication backend.
    """

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_access_to_allauth_views(self):
        """
        Test if the authenticated and unpaired user can access to all the
        ``djago-allauth`` views that require login.
        """

        # If everything works with these values, it also
        # works with account_set_password
        viewnames = [
            "account_logout",
            "account_inactive",
            "account_reauthenticate",
            "account_email",
            "account_change_password",
        ]

        for viewname in viewnames:
            with self.subTest(viewname=viewname):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(resp.status_code, HTTPStatus.OK)


@override_settings(
    AUTHENTICATION_BACKENDS=["tests.backends.LatchAuthenticationAllauthBackend"],
    ROOT_URLCONF="tests.urls_allauth",
)
@modify_settings(
    MIDDLEWARE={"append": "allauth.account.middleware.AccountMiddleware"},
    INSTALLED_APPS={"append": ["allauth", "allauth.account"]},
)
class PairedUserTests(BasePairedUserTests):
    """
    Tests for an already paired authenticated user using the ``django-allauth``
    authentication process.
    """

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_access_to_allauth_views(self):
        """
        Test if the authenticated and paired user can access to all the
        ``djago-allauth`` views that require log in.
        """

        # If everything works with these values, it also
        # works with account_set_password
        viewnames = [
            "account_logout",
            "account_inactive",
            "account_reauthenticate",
            "account_email",
            "account_change_password",
        ]

        for viewname in viewnames:
            with self.subTest(viewname=viewname):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(resp.status_code, HTTPStatus.OK)


@modify_settings(
    MIDDLEWARE={"append": "allauth.account.middleware.AccountMiddleware"},
    INSTALLED_APPS={"append": ["allauth", "allauth.account"]},
)
@override_settings(
    AUTHENTICATION_BACKENDS=["tests.backends.LatchAuthenticationAllauthBackend"],
    ROOT_URLCONF="tests.urls_allauth",
)
class LatchBackendAllauthTestCase(BaseLatchBackendTestCase):
    """
    Tests the ``django-allauth`` default authentication backend modified
    with the Latch integration.
    """
