"""
Tests for the pairing and unpairing operations as a whole.
"""

# SPDX-License-Identifier: BSD-3-Clause

from http import HTTPStatus
from unittest.mock import patch, Mock

from django.test import TestCase
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

from latch_sdk.exceptions import TokenNotFound, ApplicationAlreadyPaired, LatchError

from django_latch2.forms import PairLatchForm
from django_latch2.models import LatchUserConfig

from ..base import (
    LoggedInTestCase,
    CreateLatchConfigMixin,
    mock_status_true,
    mock_status_false,
    reverse,
)


class AnonymousUserTests(TestCase):
    """
    Test pairing and unpairing with an anonymous user.
    """

    def test_operation(self):
        """
        The user must be logged in to pair or unpair its account.
        """

        for operation, viewname, data in [
            ("pair", "django_latch2_pair", {"token": "doesnotmattertoken"}),
            ("unpair", "django_latch2_unpair", None),
        ]:
            with self.subTest(operation=operation):
                resp = self.client.get(reverse(viewname))
                self.assertRedirects(
                    resp, reverse(settings.LOGIN_URL, query={"next": reverse(viewname)})
                )

                resp = self.client.post(reverse(viewname), data=data)
                self.assertRedirects(
                    resp, reverse(settings.LOGIN_URL, query={"next": reverse(viewname)})
                )

    def test_access_view_decorator(self):
        """
        ``paired_user_required`` and ``paired_user_required`` decorators redirect anonymous users
        the access to the login URL.
        """

        for decorator, viewname in [
            ("paired_user_required", "require_paired_view_class"),
            ("unpaired_user_required", "require_unpaired_view_class"),
        ]:
            with self.subTest(decorator=decorator):
                resp = self.client.get(reverse(viewname))
                self.assertRedirects(
                    resp, reverse(settings.LOGIN_URL, query={"next": reverse(viewname)})
                )


ACCOUNT_ID1 = get_random_string(64)


@patch(
    "latch_sdk.syncio.LatchSDK.account_status", new=Mock(return_value=mock_status_true)
)
class UnpairedUserTests(LoggedInTestCase):
    """Tests for an unpaired authenticated user."""

    @classmethod
    def valid_data(cls):
        """Return a set of valid user data and an account id."""
        return {
            "username": "alice",
            "email": "alice@example.com",
            "raw_password": "superpassword",
            "account_id": ACCOUNT_ID1,
        }

    @property
    def user_lookup_kwargs(self):
        """
        Return query arguments for querying the user registered.

        Copied from
        https://github.com/ubernostrum/django-registration/blob/trunk/tests/base.py.
        """
        UserModel = get_user_model()  # pylint: disable=invalid-name
        return {UserModel.USERNAME_FIELD: "alice"}

    def test_pairing_get(self):
        """
        The HTTP ``GET`` method to the pairing view uses the appropiate
        template and populates the pairing form into the context.
        """

        resp = self.client.get(reverse("django_latch2_pair"))
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(resp, "django_latch2/pair_account_form.html")
        self.assertIsInstance(resp.context["form"], PairLatchForm)

    def test_unpairing(self):
        """
        An unpaired user should not be able to access the unpair view.
        """

        resp = self.client.get(reverse("django_latch2_unpair"))
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    @patch(
        "latch_sdk.syncio.LatchSDK.account_pair",
        new=Mock(side_effect=TokenNotFound("", "")),
    )
    def test_token_not_found(self):
        """Pair with an invalid token."""
        resp = self.client.post(
            reverse("django_latch2_pair"), data={"token": "invalid token"}
        )
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertFormError(
            form=resp.context["form"],
            field="token",
            errors=PairLatchForm.NOT_FOUND_TOKEN_MESSAGE,
        )

    @patch(
        "latch_sdk.syncio.LatchSDK.account_pair",
        new=Mock(side_effect=ApplicationAlreadyPaired("", "")),
    )
    def test_already_pair_account(self):
        """
        Pair a user that was paired during the validation of the form.

        If the user is already paired when it accessed the correspondent view,
        it wouldn't be able to access to it.
        """

        resp = self.client.post(
            reverse("django_latch2_pair"), data={"token": "invalid token"}
        )
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertFormError(
            form=resp.context["form"],
            field="token",
            errors=PairLatchForm.ALREADY_PAIRED_MESSAGE,
        )

    @patch("latch_sdk.syncio.LatchSDK.account_pair", new=Mock(return_value=ACCOUNT_ID1))
    def test_no_pairing_on_get(self):
        """Pairing only occurs on HTTP ``POST``, not ``GET``."""
        resp = self.client.get(
            reverse("django_latch2_pair"), data={"token": "valid token"}
        )
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertFalse(LatchUserConfig.objects.filter(user=self.user).exists())

    @patch("latch_sdk.syncio.LatchSDK.account_pair", new=Mock(return_value=ACCOUNT_ID1))
    def test_pairing_success_url(self):
        """
        Valid pairing redirects to the success URL.
        """

        resp = self.client.post(
            reverse("django_latch2_pair"), data={"token": "valid token"}
        )
        self.assertRedirects(resp, reverse("django_latch2_pair_complete"))

    @patch("latch_sdk.syncio.LatchSDK.account_pair", new=Mock(return_value=ACCOUNT_ID1))
    def test_pairing_success_is_paired(self):
        """
        Valid pairing sets the user as paired.
        """

        resp = self.client.post(
            reverse("django_latch2_pair"), data={"token": "valid token"}
        )
        self.assertRedirects(resp, reverse("django_latch2_pair_complete"))
        self.assertTrue(LatchUserConfig.objects.filter(user=self.user).exists())
        latch_config = LatchUserConfig.objects.get(user=self.user)
        self.assertEqual(latch_config.account_id, ACCOUNT_ID1)

    def test_unpaired_user_required_decorator(self):
        """
        The unpaired_user_required decorator allows the access to unpaired users.
        """

        for deco_type, viewname in [
            ("instance", "require_unpaired_view_instance"),
            ("class", "require_unpaired_view_class"),
        ]:
            with self.subTest(decorator_type=deco_type):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(resp.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(
                    resp, "django_latch2/require_unpaired_user.html"
                )

    def test_paired_user_required_decorator(self):
        """
        The paired_user_required forbids the access to unpaired users.
        """

        for deco_type, viewname in [
            ("instance", "require_paired_view_instance"),
            ("class", "require_paired_view_class"),
        ]:
            with self.subTest(decorator_type=deco_type):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(
                    resp.status_code, HTTPStatus.FORBIDDEN, msg=f"{resp.serialize()}"
                )


ACCOUNT_ID2 = get_random_string(64)


class PairedUserTests(CreateLatchConfigMixin, LoggedInTestCase):
    """Tests for an already paired authenticated user."""

    @classmethod
    def valid_data(cls):
        """Return a set of valid user data and an account id."""
        return {
            "username": "bob",
            "email": "bob@example.com",
            "raw_password": "superpassword",
            "account_id": ACCOUNT_ID2,
        }

    @property
    def user_lookup_kwargs(self):
        """
        Return query arguments for querying the user registered.

        Copied from https://github.com/ubernostrum/django-registration/blob/trunk/tests/base.py.
        """
        UserModel = get_user_model()  # pylint: disable=invalid-name
        return {UserModel.USERNAME_FIELD: "bob"}

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_pairing(self):
        """
        An already paired user should not be able to access the pair view.
        """

        resp = self.client.get(reverse("django_latch2_pair"))
        self.assertEqual(resp.status_code, HTTPStatus.FORBIDDEN)

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_unpairing_get(self):
        """
        The HTTP ``GET`` method to the unpairing view use the appropiate
        template.
        """

        resp = self.client.get(reverse("django_latch2_unpair"))
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(resp, "django_latch2/unpair_account.html")

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_no_unpairing_on_get(self):
        """
        Unpairing only occurs on HTTP ``POST``, not ``GET``.
        """

        resp = self.client.get(reverse("django_latch2_unpair"))
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertTrue(LatchUserConfig.objects.filter(user=self.user).exists())

    @patch("latch_sdk.syncio.LatchSDK.account_unpair", new=Mock(return_value=True))
    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_success_is_unpaired(self):
        """
        Valid unpairing sets the user as unpaired.
        """

        resp = self.client.post(reverse("django_latch2_unpair"))
        self.assertRedirects(resp, reverse("django_latch2_unpair_complete"))
        self.assertFalse(LatchUserConfig.objects.filter(user=self.user).exists())

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_paired_user_required_decorator(self):
        """
        The paired_user_required decorator allows the access to paired users.
        """

        for deco_type, viewname in [
            ("instance", "require_paired_view_instance"),
            ("class", "require_paired_view_class"),
        ]:
            with self.subTest(decorator_type=deco_type):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(resp.status_code, HTTPStatus.OK)
                self.assertTemplateUsed(resp, "django_latch2/require_paired_user.html")

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_unpair_user_required_decorator(self):
        """
        The unpaired_user_required forbids the access to paired users.
        """

        for deco_type, viewname in [
            ("instance", "require_unpaired_view_instance"),
            ("class", "require_unpaired_view_class"),
        ]:
            with self.subTest(decorator_type=deco_type):
                resp = self.client.get(reverse(viewname))
                self.assertEqual(
                    resp.status_code, HTTPStatus.FORBIDDEN, msg=f"{resp.serialize()}"
                )

    @patch(
        "latch_sdk.syncio.LatchSDK.account_unpair",
        new=Mock(side_effect=LatchError("", "")),
    )
    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_unpairing_failure(self):
        """Error during unpairing."""
        resp = self.client.post(reverse("django_latch2_unpair"))
        self.assertEqual(resp.status_code, HTTPStatus.OK)
        self.assertIn("unpair_error", resp.context)
        self.assertIn("message", resp.context["unpair_error"])
        self.assertIn("code", resp.context["unpair_error"])

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_false),
    )
    def test_login_when_off(self):
        """
        A user who has its latch on should not be able to login.
        """

        self.client.logout()
        logged = self.client.login(
            username=self.user.username,
            password=self.valid_data()["raw_password"],
        )
        self.assertFalse(logged)
