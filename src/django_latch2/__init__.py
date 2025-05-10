"""
Telefonica's Latch support for Django.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

from latch_sdk.syncio import LatchSDK

HTTP_BACKENDS = {
    "http": "latch_sdk.syncio.pure.Latch",
    "httpx": "latch_sdk.syncio.httpx.Latch",
    "requests": "latch_sdk.syncio.requests.Latch",
}


def check_http_backend(chosen_backend):
    """
    Check if the chosen backend is between those available.
    """

    if chosen_backend not in HTTP_BACKENDS:
        raise ImproperlyConfigured(
            f"The LATCH_HTTP_BACKEND setting cannot be {chosen_backend}, the only valid values are 'http', 'requests' or 'httpx'."
        )


def get_latch_api():
    """Return the Latch SDK for accessing Latch's API."""
    LATCH_HTTP_BACKEND = getattr(settings, "LATCH_HTTP_BACKEND", "http")  # pylint: disable=invalid-name
    check_http_backend(LATCH_HTTP_BACKEND)
    core_class = import_string(HTTP_BACKENDS[LATCH_HTTP_BACKEND])
    return LatchSDK(core_class(settings.LATCH_APP_ID, settings.LATCH_SECRET_KEY))
