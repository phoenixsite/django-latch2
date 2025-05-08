"""
URLconf for pairing and unpairing the user's latch.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.urls import path
from django.views.generic.base import TemplateView

from . import views

urlpatterns = [
    path("pair-latch/", views.PairLatchView.as_view(), name="django_latch2_pair"),
    path(
        "pair-latch/complete/",
        TemplateView.as_view(template_name="django_latch2/pair_complete.html"),
        name="django_latch2_pair_complete",
    ),
    path(
        "unpair-latch/",
        views.UnpairLatchView.as_view(),
        name="django_latch2_unpair",
    ),
    path(
        "unpair-latch/complete/",
        TemplateView.as_view(template_name="django_latch2/unpair_complete.html"),
        name="django_latch2_unpair_complete",
    ),
]
