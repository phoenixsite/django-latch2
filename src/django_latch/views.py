"""
Views for pairing and unpairing a user.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _

from latch_sdk.exceptions import LatchError

from . import get_latch_api
from .forms import PairLatchForm
from .models import LatchUserConfig, is_paired
from .exceptions import UnpairingLatchError
from .mixins import UnpairedUserRequiredMixin, PairedUserRequiredMixin


class PairLatchView(UnpairedUserRequiredMixin, FormView):
    """
    Implement the pairing operation for an authenticated and unpaired user.

    It is a subclass of :class:`~django_latch.mixins.UnpairedUserRequiredMixin`,
    so only authenticated users without the latch configured can access it.

    .. automethod:: form_valid

    """

    ALREADY_PAIRED_MESSAGE = _("Your account is already paired.")

    form_class = PairLatchForm
    template_name = "django_latch/pair_account_form.html"
    success_url = reverse_lazy("django_latch_pair_complete")

    def form_valid(self, form):
        """
        If the form is valid, attempt to pair the user account to the Latch service
        and redirect to the success URL. If a :class:`django_latch:exceptions.PairingLatchError`
        is raised, instead re-render the form and include information about the error in the
        template context.

        :param django_latch.forms.PairLatchForm form: The token form to use.
        """

        form.pair_account(self.request.user)
        return super().form_valid(form)


class UnpairLatchView(PairedUserRequiredMixin, TemplateView):
    """
    Implement the unpairing operation for a authenticated paired user.

    It is a subclass of :class:`~django_latch.mixins.PairedUserRequiredMixin`,
    so only authenticated users with the latch configured can access it.

    .. automethod:: unpair_account

    .. automethod:: post

    .. automethod:: check_user
    """

    NOT_PAIRED_MESSAGE = _("Your account is not paired with Latch.")

    template_name = "django_latch/unpair_account.html"
    success_url = reverse_lazy("django_latch_unpair_complete")

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Attempt to unpair the user account from the Latch service and
        redirect to the success URL. If a
        :class:`django_latch:execptions.UnpairingLatchError` is raised, re-render
        the view and include information about the error in the template context.
        """

        extra_context = {}

        try:
            self.unpair_account()
        except UnpairingLatchError as exc:
            extra_context["unpair_error"] = {
                "message": exc.message,
                "code": exc.code,
                "params": exc.params,
            }
        else:
            return HttpResponseRedirect(self.success_url)

        context_data = self.get_context_data()
        context_data.update(extra_context)
        return self.render_to_response(context_data)

    def unpair_account(self):
        """
        Unpair the user account from the Latch service.
        """

        self.check_user()
        config = LatchUserConfig.objects.get(user=self.request.user)
        try:
            latch_api = get_latch_api()
            latch_api.account_unpair(config.account_id)
        except LatchError as exc:
            raise UnpairingLatchError(exc.message, exc.code) from exc

        config.delete()

    def check_user(self):
        """
        Check if the logged user doesn't have its account latched,
        raising ``UnpairingLatchError`` if so.
        """

        if not is_paired(self.request.user):
            raise UnpairingLatchError(self.NOT_PAIRED_MESSAGE, "not_paired")
