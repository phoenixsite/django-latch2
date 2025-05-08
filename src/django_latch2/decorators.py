"""
Function decorators that check the status of a user according to the configuration of its latch.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

from .models import is_paired


def first_authenticated_then_other(condition_func, user):
    """
    Check if ``user`` is authenticated and another condition, returning
    ``True`` if so. If ``user`` is not authenticated, return ``False``.
    But if ``user`` is authenticated but the condition is not met, then
    a :class:`django.core.exceptions.PermissionDenied` is raised.

    This is used for implementing a class-based view or function decorator
    We don't use directly the returned value of condition_func because it is
    necessary to check first if the user is authenticated.
    """
    if user.is_authenticated:
        if condition_func(user):
            return True
        raise PermissionDenied
    return False


def paired_user_required(function=None):
    """
    Decorator for views that checks that authenticated user is paired with
    the Latch service.
    """

    actual_decorator = user_passes_test(
        lambda u: first_authenticated_then_other(is_paired, u)
    )
    if function:
        return actual_decorator(function)
    return actual_decorator  # pragma: no cover


def unpaired_user_required(function=None):
    """
    Decorator for views that checks that the authenticated user is not paired with
    the Latch service.
    """

    def not_paired(user):
        """
        Negative of ``is_paired``. We need it for ``first_authenticated_then_other``.
        """
        return not is_paired(user)

    actual_decorator = user_passes_test(
        lambda u: first_authenticated_then_other(not_paired, u)
    )
    if function:
        return actual_decorator(function)
    return actual_decorator  # pragma: no cover
