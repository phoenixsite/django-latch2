"""
Mixins that check the status of a user according to the configuration of its latch.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.mixins import AccessMixin

from .models import is_paired


class UnpairedUserRequiredMixin(AccessMixin):
    """
    Verify that the current user is paired with the Latch service.

    It has the same the behaviour as :func:`~django_latch.decorators.unpaired_user_required`,
    which is the following:

    * If the user isn't logged in, it redirects to :setting:`settings.LOGIN_URL <LOGIN_URL>`
      passing the current absolute path in the query string.
    * If the user is authenticated but paired, then the decorator will
      raise :exc:`~django.core.exceptions.PermissionDenied`, prompting
      `the 403 (HTTP Forbidden) view
      <https://docs.djangoproject.com/en/5.2/ref/views/#http-forbidden-view>`_
      instead of redirecting to the login page.

    This mixin implies that the user must be logged in, so using
    :class:`~django.contrib.auth.mixins.LoginRequiredMixin` is not necessary when a
    view inherit from :class:`~django_latch.mixins.UnpairedUserRequiredMixin`.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        """
        Check that the user account is already paired with Latch,
        forbidding the access if so.
        """

        if not request.user.is_authenticated or is_paired(self.request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class PairedUserRequiredMixin(AccessMixin):
    """
    Verify that the current user is not paired with the Latch service.

    It has the same the behaviour as
    :func:`~django_latch.decorators.paired_user_required`, which is the
    following:

    * If the user isn't logged in, it redirects to :setting:`settings.LOGIN_URL <LOGIN_URL>`
      passing the current absolute path in the query string.
    * If the user is authenticated but unpaired, then the decorator will
      raise :exc:`~django.core.exceptions.PermissionDenied`, prompting
      `the 403 (HTTP Forbidden) view
      <https://docs.djangoproject.com/en/5.2/ref/views/#http-forbidden-view>`_
      instead of redirecting to the login page.

    This mixin implies that the user must be logged in, so using
    :class:`~django.contrib.auth.mixins.LoginRequiredMixin` is not necessary
    when a view inherit from :class:`~django_latch.mixins.PairedUserRequiredMixin`.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        """
        Check that the user account is not paired with Latch,
        forbidding the access if so.
        """

        if not request.user.is_authenticated or not is_paired(self.request.user):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)
