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


def get_latch_api():
    """
    Return the Latch SDK for accessing Latch's API.

    If the setting :data:`LATCH_HTTP_BACKEND` is not set, the default
    would be the 'http' one, which does not require a third-party package.
    """

    http_backend = getattr(settings, "LATCH_HTTP_BACKEND", "http")  # pylint: disable=invalid-name

    try:
        core_class = import_string(HTTP_BACKENDS[http_backend])
    except KeyError as exc:
        raise ImproperlyConfigured(
            f"The LATCH_HTTP_BACKEND setting cannot be {http_backend}, the only "
            "valid values are 'http', 'requests' or 'httpx'."
        ) from exc
    return LatchSDK(core_class(settings.LATCH_APP_ID, settings.LATCH_SECRET_KEY))
