"""
Form for latch pairing.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from latch_sdk.exceptions import TokenNotFound, ApplicationAlreadyPaired

from .models import LatchUserConfig
from . import get_latch_api

# pylint: disable=raise-missing-from


class PairLatchForm(forms.Form):
    """
    A form for pairing the user account to the Latch service.

    .. automethod:: clean_token

    .. automethod:: pair_account
    """

    NOT_FOUND_TOKEN_MESSAGE = _("The token you provided hasn't been found.")
    ALREADY_PAIRED_MESSAGE = _("Your account is already paired.")

    token = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.account_id = None

    def clean_token(self):
        """
        Validate the token with the Latch service.

        Because the validation of the token must be done with Latch and it
        returns the account id if the token is valid, we cached the account id.

        If the token is not found by the Latch service, then a
        :exc:`django.core.exceptions.ValidationError` with the code
        ``'not_found'`` is raised.
        If the user has already pair its account, then a
        :exc:`django.core.exceptions.ValidationError` is raised with
        the code ``'already_paired'``.
        """

        token = self.cleaned_data["token"]
        try:
            latch_api = get_latch_api()
            self.account_id = latch_api.account_pair(token)
            return token
        except TokenNotFound:
            raise ValidationError(self.NOT_FOUND_TOKEN_MESSAGE, code="not_found")

        # Though in theory this must never happen, it is checked if the same Latch application id
        # is being used somewhere else or the user was paired in the middle of the form
        # validation.
        except ApplicationAlreadyPaired:
            raise ValidationError(self.ALREADY_PAIRED_MESSAGE, code="already_paired")

    def pair_account(self, user):
        """
        Pair the user account with a Latch account id.

        As the account id has been already obtained by checking
        the validity of the token, this method only creates the instance
        for storing the account id.
        """

        config = LatchUserConfig.objects.create(user=user, account_id=self.account_id)
        return config
