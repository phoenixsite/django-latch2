from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from latch.models import LatchSetup
from . import LatchTest


class APITests(LatchTest):
    @patch("latch.latch_sdk_python.latch.Latch.__init__")
    def test_api_called_with_correct_settings(self, mock_latch):
        mock_latch.return_value = None

        LatchSetup.instance()

        mock_latch.assert_called_once_with(
            "abcdefghijklmnopqrst", "abcdefghijklmnopqrstuvwxyzabcdefghijklmno"
        )

    @override_settings(LATCH_APP_ID=None)
    def test_exception_raised_when_app_id_not_configured(self):
        with self.assertRaises(ImproperlyConfigured):
            LatchSetup.instance()

    @override_settings(LATCH_APP_SECRET=None)
    def test_exception_raised_when_app_secret_not_configured(self):
        with self.assertRaises(ImproperlyConfigured):
            LatchSetup.instance()

    def test_configured_app_returns_correct_app_id(self):
        self.assertEqual(LatchSetup.appid(), "abcdefghijklmnopqrst")
