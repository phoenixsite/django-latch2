import json

from http.client import HTTPException

from unittest.mock import patch

from django.contrib.auth.models import AnonymousUser
from django.test import override_settings

from latch import views

from . import FactoryTestMixin, LatchTest

class UnpairingTests(FactoryTestMixin, LatchTest):
    def test_pair_form_not_accesible_for_anonymous_user(self):
        request = self.factory.get("/pair")
        request.user = AnonymousUser()

        response = views.pair(request)

        self.assertEqual(response.status_code, 302)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_unpair_works_correctly(self, mock_unpair):
        mock_unpair.return_value = {
            json.dumps({})
        }
        data = {"latch_confirm": True}
        request = self.factory.post("/unpair", data=data)
        request.user = self.paired_user

        response = views.unpair(request)

        self.assertContains(response, "Latch removed from your account")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_show_warning_if_account_is_not_latched(self, mock_unpair):
        data = {"latch_confirm": True}
        request = self.factory.post("/unpair", data=data)
        request.user = self.unpaired_user

        response = views.unpair(request)

        self.assertContains(response, "Your account is not latched")
        self.assertEqual(mock_unpair.called, False)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_shows_error_message_when_cannot_connect_to_latch(self, mock_unpair):
        mock_unpair.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_confirm": True}
        request = self.factory.post("/unpair", data=data)
        request.user = self.paired_user

        response = views.unpair(request)

        self.assertContains(response, "Error unpairing the account")

    @override_settings(DEBUG=True)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_error_message_shown_when_debug_is_true(self, mock_unpair):
        mock_unpair.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_confirm": True}
        request = self.factory.post("/unpair", data=data)
        request.user = self.paired_user

        response = views.unpair(request)

        self.assertContains(response, "Error unpairing the account: HTTP Generic Exception")

    @override_settings(DEBUG=False)
    @patch("latch.latch_sdk_python.latchapp.LatchApp.unpair")
    def test_error_message_hidden_when_debug_is_false(self, mock_unpair):
        mock_unpair.side_effect = HTTPException("HTTP Generic Exception")

        data = {"latch_confirm": True}
        request = self.factory.post("/unpair", data=data)
        request.user = self.paired_user

        response = views.unpair(request)

        self.assertContains(response, "Error unpairing the account")
