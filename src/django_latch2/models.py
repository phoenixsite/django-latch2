"""
Models to associate a user to the Latch service.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.db import models
from django.contrib.auth import get_user_model

UserModel = get_user_model()


def is_paired(user):
    """
    Check if a user has configured the Latch service, returning
    ``True`` if so, ``False`` otherwise.
    """
    return LatchUserConfig.objects.filter(user=user).exists()


class LatchUserConfig(models.Model):
    """
    Store the necessary configuration to associate
    a user to the Latch service.

    The only parameter required is the account id, which is
    a code with 64 characters.
    """

    user = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        related_name="latch_config",
    )
    account_id = models.CharField(unique=True, max_length=64, blank=False)
