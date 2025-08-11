"""
Tests for the behaviour of the backends that use the Latch service.
"""

# SPDX-License-Identifier: BSD-3-Clause

from unittest.mock import patch, Mock
from django.test import TestCase
from django.core.exceptions import PermissionDenied
from django.utils.crypto import get_random_string

from django_latch.backends import can_pass_latch, LatchDefaultModelBackend

from .base import CreateLatchConfigMixin, mock_status_true, mock_status_false


class LatchBackendTestCase(CreateLatchConfigMixin, TestCase):
    """
    Tests for the backends.
    """

    @classmethod
    def valid_data(cls):
        """Return a set of valid user data and an account id."""
        return {
            "username": "andrew",
            "email": "andrew@example.com",
            "raw_password": "superpassword",
            "account_id": get_random_string(64),
        }

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_is_latch_on_when_on(self):
        """
        A user whose account_id returns an on status can authenticate.
        """

        self.assertTrue(can_pass_latch(self.user))

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_false),
    )
    def test_can_pass_latch_when_off(self):
        """
        A user whose account_id returns an off status cannot authenticate.
        """

        self.assertFalse(can_pass_latch(self.user))

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_false),
    )
    def test_cannot_authenticate(self):
        """
        If the latch is set, then the ``user_can_authenticate`` method must raise a
        ``PermissionDenied`` exception.
        """
        with self.assertRaises(PermissionDenied):
            LatchDefaultModelBackend().user_can_authenticate(self.user)

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def test_can_authenticate(self):
        """
        If the latch is not set, then the user can authenticate.
        """

        self.assertTrue(LatchDefaultModelBackend().user_can_authenticate(self.user))
