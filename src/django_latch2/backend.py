"""
Authentication backends that define the behaviour for cheking
a user's latch.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import PermissionDenied
from django.utils.crypto import get_random_string

from latch_sdk.exceptions import LatchError

from . import get_latch_api

UserModel = get_user_model()


def can_pass_latch(user):
    """
    Check the ``user``'s latch state. Return ``True`` if the latch is open,
    ``False`` if it's closed.
    """

    can_pass = True
    latch_api = get_latch_api()
    try:
        l_config = user.latch_config
    except UserModel.latch_config.RelatedObjectDoesNotExist:
        # In order to prevent an attacker knowing a user has configured
        # the Latch service, we need to make a mock call to the API
        # so the latency difference between a user with a configured latch
        #  and a user without a configured latch.
        try:
            latch_api.account_status(get_random_string(64))
        except LatchError:
            pass
    else:
        status = latch_api.account_status(l_config.account_id)
        can_pass = status.status

    return can_pass


class LatchModelBackendMixin:
    """
    A mixin for authentication backends that checks if the user has its latch on.
    """

    # pylint: disable=too-few-public-methods

    def user_can_authenticate(self, user):
        """
        Reject users who have their latch on. Users without the Latch
        configured are allowed.
        """
        if not can_pass_latch(user):
            raise PermissionDenied()
        return super().user_can_authenticate(user)


class LatchDefaultModelBackend(LatchModelBackendMixin, ModelBackend):
    """
    A subclass of :class:`django.contrib.auth.backends.ModelBackend` that also checks if
    the user's latch is on.

    This backend is useful for a fast integration of the Latch service
    into a Django project that uses the default authentication backend,
    but it has `the same limitations
    <https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#specifying-authentication-backends>`_.
    """
