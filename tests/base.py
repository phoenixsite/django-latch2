"""
Base classes for other test cases to inherit from.
"""

# SPDX-License-Identifier: BSD-3-Clause

from unittest.mock import patch, Mock

from django.contrib.auth import get_user_model
from django.test import TestCase

from latch_sdk.models import Status

from django_latch2.models import LatchUserConfig

ACCOUNT_ID = "a" * 64


class CreateUserMixin:
    """
    Force a subclass to create a user.
    """

    @classmethod
    def valid_data(cls):
        """Return a set of valid user data for the test to run."""
        raise NotImplementedError(
            "Subclasses of CreateUserMixin must implement the class method valid_data()."
        )

    @classmethod
    def setUpTestData(cls):  # pylint: disable=invalid-name
        """
        A user is created with the data given by the class method ``valid_data``.
        """

        UserModel = get_user_model()  # pylint: disable=invalid-name
        cls.user = UserModel.objects.create_user(
            username=cls.valid_data()["username"],
            email=cls.valid_data()["email"],
            password=cls.valid_data()["raw_password"],
        )


class CreateLatchConfigMixin(CreateUserMixin):
    """
    Force a subclass to create a latch configuration for the user.
    """

    @classmethod
    def valid_data(cls):
        """Return a set of valid user data and an account id for the test to run."""
        raise NotImplementedError(
            "Subclasses of CreateLatchConfigMixin must implement the class method valid_data()."
        )

    @classmethod
    def setUpTestData(cls):
        """
        The latch configuration of the previously created user is created.
        """

        super().setUpTestData()
        cls.latch_config = LatchUserConfig.objects.create(
            user=cls.user, account_id=cls.valid_data()["account_id"]
        )


mock_status_true = Status.build_from_dict({"operation_id": 1, "status": "on"})
mock_status_false = Status.build_from_dict({"operation_id": 1, "status": "off"})


class LoggedInTestCase(CreateUserMixin, TestCase):  # pylint: disable=abstract-method
    """
    The test client is logged in with a valid user.
    """

    @patch(
        "latch_sdk.syncio.LatchSDK.account_status",
        new=Mock(return_value=mock_status_true),
    )
    def setUp(self):
        """
        The client is logged with the ``CreateUserMixin`` user.
        """

        super().setUp()
        logged = self.client.login(
            username=self.user.username,
            password=self.valid_data()["raw_password"],
        )

        if not logged:
            raise RuntimeError("Couldn't logged in user.")
