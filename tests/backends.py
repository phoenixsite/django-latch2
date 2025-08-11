"""
Custom backend based on the provided by ``django-allauth``.
"""

# SPDX-License-Identifier: BSD-3-Clause

from allauth.account.auth_backends import AuthenticationBackend

from django_latch.backends import LatchModelBackendMixin


class LatchAuthenticationAllauthBackend(LatchModelBackendMixin, AuthenticationBackend):
    """
    ``django-allauth``'s backend with Latch integration.
    """
