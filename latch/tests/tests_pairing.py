import json

from http.client import HTTPException

from unittest.mock import patch

from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User, AnonymousUser

from latch import views
from latch.models import UserProfile

from latch import latch_sdk_python as sdk

from . import FactoryTestMixin, LatchTest


class PairingTests(FactoryTestMixin, LatchTest):
    def setUp(self):
        # Override the unpaired user to be written on an per-test basis.
        # If not, once we run the test_pairing_with_correct_code
        # tests reliying of unpaired users will fail
        self.unpaired_user = User.objects.create_user(
            username="unpaired_user", email="unpaired_user@mail.com", password="password"
        )

    def test_pair_form_not_accesible_for_anonymous_user(self):
        request = self.factory.get("/pair")
        request.user = AnonymousUser()

        response = views.pair(request)

        self.assertEqual(response.status_code, 302)

    def test_pair_form_shown_in_unpaired_account(self):
        request = self.factory.get("/pair")
        request.user = self.unpaired_user

        response = views.pair(request)

        self.assertEqual(response.status_code, 200)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_with_correct_code(self, mock_pair):
        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps({"data": {"accountId": "123456"}})
        )

        data = {"latch_pin": "correc"}
        request = self.factory.post("/pair", data=data)
        request.user = self.unpaired_user

        response = views.pair(request)

        self.assertContains(response, "Account paired with Latch")
        user_profile = None
        try:
            user_profile = UserProfile.objects.get(user=self.unpaired_user)
        except ObjectDoesNotExist:
            self.fail("Profile object has not been created")

        self.assertEqual(user_profile.latch_accountId, "123456")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_already_paired_user_shows_error(self, mock_pair):
        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": "",
                    "error": {
                        "code": 205,
                        "message": "Account and application already paired",
                    },
                }
            )
        )

        data = {"latch_pin": "incorr"}
        request = self.factory.post("/pair", data=data)
        request.user = self.paired_user

        response = views.pair(request)

        self.assertContains(response, "Account is already paired")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pairing_with_wrong_code_shows_error(self, mock_pair):
        mock_pair.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": "",
                    "error": {"code": 206, "message": "Token not found or expired"},
                }
            )
        )

        data = {"latch_pin": "incorr"}
        request = self.factory.post("/pair", data=data)
        request.user = self.unpaired_user

        response = views.pair(request)

        self.assertContains(response, "Account not paired with Latch")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.pair")
    def test_pair_failed(self, mock_pair):
        mock_pair.side_effect = HTTPException("HTTP Generic Exception")
        data = {"latch_pin": "correc"}
        request = self.factory.post("/pair", data=data)
        request.user = self.unpaired_user

        response = views.pair(request)

        self.assertContains(response, "Error pairing the account")
