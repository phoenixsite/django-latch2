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
    Decorator for views that checks that the authenticated user is paired with
    the Latch service.

    It has the same the behaviour as :class:`~django_latch.mixins.PairedUserRequiredMixin`,
    which is the following:

    * If the user isn't logged in, it redirects to :setting:`settings.LOGIN_URL <LOGIN_URL>`
      passing the current absolute path in the query string.
    * If the user is authenticated but unpaired, then the decorator will
      raise :exc:`~django.core.exceptions.PermissionDenied`, prompting
      `the 403 (HTTP Forbidden) view
      <https://docs.djangoproject.com/en/5.2/ref/views/#http-forbidden-view>`_
      instead of redirecting to the login page.

    This decorator implies that a user must be logged in, so using
    :func:`~django.contrib.auth.decorators.login_required` is not necessary
    when :func:`~django_latch.decorators.paired_user_required` is present.
    """

    actual_decorator = user_passes_test(
        lambda u: first_authenticated_then_other(is_paired, u)
    )
    if function:
        return actual_decorator(function)
    return actual_decorator  # pragma: no cover


def unpaired_user_required(function=None):
    """
    Decorator for views that checks that the authenticated user is not
    paired with the Latch service.

    It has the same the behaviour as :class:`~django_latch.mixins.UnpairedUserRequiredMixin`,
    which is the following:

    * If the user isn't logged in, it redirects to :setting:`settings.LOGIN_URL <LOGIN_URL>`
      passing the current absolute path in the query string.
    * If the user is authenticated but paired, then the decorator will
      raise :exc:`~django.core.exceptions.PermissionDenied`, prompting
      `the 403 (HTTP Forbidden) view
      <https://docs.djangoproject.com/en/5.2/ref/views/#http-forbidden-view>`_
      instead of redirecting to the login page.

    This decorator implies that a user must be logged in, so using
    :func:`~django.contrib.auth.decorators.login_required` is not necessary
    when :func:`~django_latch.decorators.unpaired_user_required` is present.
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
