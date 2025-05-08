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
