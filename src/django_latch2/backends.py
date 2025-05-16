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
        #  and a user without is not significant enough.
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

    In order to be able to use Latch and not provoke any error,
    this class must be the first one to be inherited from when creating
    a custom authentication backend.

    .. automethod:: user_can_authenticate

    .. automethod:: get_user
    """

    # pylint: disable=too-few-public-methods

    def user_can_authenticate(self, user):
        """
        Reject users who have their latch on. Users without the Latch
        configured are allowed.

        If the user's latch is on, i.e. it cannot access the
        application, then a :exc:`~django.core.exceptions.PermissionDenied`
        is raised.

        Though it may seems this break the original "contract" of the
        :meth:`~django.contrib.auth.backends.BaseBackend.user_can_authenticate`
        method, there is no other place to raise the exception without
        overriding the
        :meth:`~django.contrib.auth.backends.BaseBackend.authenticate` method and
        blocking the check on the rest of the authentication backends
        (which is the objective of Latch: completely block the access, though
        in future releases this can be extended and generalized).
        """

        if not can_pass_latch(user):
            raise PermissionDenied()
        return super().user_can_authenticate(user)

    def get_user(self, user_id):
        """
        Returns the user object related to ``user_id``.

        We need to override this method because we are raising
        the :exc:`~django.core.exceptions.PermissionDenied` exception in the
        method
        :meth:`django.contrib.auth.backends.BaseBackend.user_can_authenticate`
        instead of on
        :meth:`django.contrib.auth.backends.BaseBackend.authenticate`. Then,
        if we use :class:`django.contrib.auth.backends.ModelBackend` the
        exception would not be caught in
        :meth:`~django.contrib.auth.backends.ModelBackend.get_user`.

        The decision behind of raising the exception in
        :meth:`django.contrib.auth.backends.BaseBackend.user_can_authenticate`
        is because the method
        :meth:`django.contrib.auth.backends.BaseBackend.authenticate`
        is more likely to be overridden, but, of course, overriding
        :meth:`django.contrib.auth.backends.BaseBackend.get_user` may be also
        a big sacrifice.
        """

        try:
            user = UserModel._default_manager.get(pk=user_id)  # pylint: disable=protected-access
        except UserModel.DoesNotExist:
            return None
        return user if super().user_can_authenticate(user) else None


class LatchDefaultModelBackend(LatchModelBackendMixin, ModelBackend):
    """
    A subclass of :class:`django.contrib.auth.backends.ModelBackend` that also checks if
    the user's latch is on.

    This backend is useful for a fast integration of the Latch service
    into a Django project that uses the default authentication process,
    so it has `the same limitations
    <https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#specifying-authentication-backends>`_.
    """
