import json

from http.client import HTTPException

from unittest.mock import patch

from latch import views
from latch.models import LatchSetup
from latch import latch_sdk_python as sdk

from . import FactoryTestMixin, LatchTest


class StatusTest(FactoryTestMixin, LatchTest):
    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_show_yes_if_latch_is_configured(self, mock_status):
        mock_status.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": {
                        "operations": {
                            "applicationId": {
                                "status": "on",
                                "operations": {"status": "on"},
                            }
                        }
                    }
                }
            )
        )
        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.status(request)

        self.assertContains(response, "Latch is configured: <b>Yes</b>")

    def test_show_no_if_latch_is_configured(self):
        LatchSetup.objects.get(pk=1).delete()

        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.status(request)

        self.assertContains(response, "Latch is configured: <b>No</b>")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_tells_if_account_is_paired(self, mock_status):
        mock_status.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": {
                        "operations": {
                            "applicationId": {
                                "status": "on",
                                "operations": {"status": "on"},
                            }
                        }
                    }
                }
            )
        )
        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.status(request)

        self.assertContains(
            response,
            "Your accountId is: " \
            "<b>abcdefghijlkmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcdefghijkl</b>",
        )

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_tells_if_account_is_not_paired(self, mock_status):
        request = self.factory.get("/status")
        request.user = self.unpaired_user

        response = views.status(request)

        self.assertContains(response, "Your account is <b>not latched</b>")
        self.assertEqual(mock_status.called, False)

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_shows_correct_status_when_latch_is_activated(self, mock_status):
        mock_status.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": {
                        "operations": {
                            "applicationId": {
                                "status": "on",
                                "operations": {"status": "on"},
                            }
                        }
                    }
                }
            )
        )

        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.status(request)

        self.assertContains(response, "Account status: <b>on</b>")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_shows_correct_status_when_latch_is_deactivated(self, mock_status):
        mock_status.return_value = sdk.latchresponse.LatchResponse(
            json.dumps(
                {
                    "data": {
                        "operations": {
                            "applicationId": {
                                "status": "off",
                                "operations": {"status": "off"},
                            }
                        }
                    }
                }
            )
        )

        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.status(request)

        self.assertContains(response, "Account status: <b>off</b>")

    @patch("latch.latch_sdk_python.latchapp.LatchApp.status")
    def test_shows_error_message_when_cant_connect_to_latch(self, mock_status):
        mock_status.side_effect = HTTPException("HTTP Generic Exception")

        request = self.factory.get("/status")
        request.user = self.paired_user

        response = views.status(request)

        self.assertContains(response, "Latch connection error")
