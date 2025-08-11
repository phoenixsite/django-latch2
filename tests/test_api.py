"""
Tests for the Latch API configuration.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase
from django.test.utils import override_settings

# pylint: disable=import-outside-toplevel


class HTTPBackendTestCases(TestCase):
    """
    Tests that check the HTTP backend that the Latch API is using.
    """

    def test_core_http(self):
        """
        When LATCH_HTTP_BACKEND is `'http'`, then core class must be
        `latch_sdk.syncio.pure.Latch`.
        """

        from django_latch import get_latch_api

        latch_api = get_latch_api()
        from latch_sdk.syncio.pure import Latch

        self.assertEqual(type(latch_api.core), Latch)

    @override_settings(LATCH_HTTP_BACKEND="requests")
    def test_core_requests(self):
        """
        When LATCH_HTTP_BACKEND is `'requests'`, then core class must be
        `latch_sdk.syncio.requests.Latch`.
        """

        from django_latch import get_latch_api

        latch_api = get_latch_api()
        from latch_sdk.syncio.requests import Latch

        self.assertEqual(type(latch_api.core), Latch)

    @override_settings(LATCH_HTTP_BACKEND="requests")
    def test_core_httpx(self):
        """
        When LATCH_HTTP_BACKEND is `'httpx'`, then core class must be
        `latch_sdk.syncio.httpx.Latch`.
        """

        from django_latch import get_latch_api

        latch_api = get_latch_api()
        from latch_sdk.syncio.requests import Latch

        self.assertEqual(type(latch_api.core), Latch)

    @override_settings(LATCH_HTTP_BACKEND="invalid_backend")
    def test_core_invalid_backend(self):
        """
        When LATCH_HTTP_BACKEND is is not a valid one, a
        :class:`~django.core.exceptions.ImproperlyConfigured` is raised.
        """

        message = (
            "The LATCH_HTTP_BACKEND setting cannot be invalid_backend, "
            "the only valid values are 'http', 'requests' or 'httpx'."
        )
        with self.assertRaisesMessage(ImproperlyConfigured, message):
            from django_latch import get_latch_api

            get_latch_api()
