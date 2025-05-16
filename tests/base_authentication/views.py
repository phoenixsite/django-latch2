"""
View classes to test the funtions decorators.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from django_latch2.decorators import paired_user_required, unpaired_user_required


@method_decorator(paired_user_required, name="dispatch")
class RequirePairedUserWithClassDecoratorView(TemplateView):
    """
    View for testing the ``paired_user_required`` as a class
    decorator.
    """

    template_name = "django_latch2/require_paired_user.html"


@method_decorator(unpaired_user_required, name="dispatch")
class RequireUnPairedUserWithMethodDecoratorView(TemplateView):
    """
    View for testing the ``unpaired_user_required`` as a class
    decorator.
    """

    template_name = "django_latch2/require_unpaired_user.html"
