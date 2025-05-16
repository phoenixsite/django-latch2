"""
URLConf used for testing.
"""

# SPDX-License-Identifier: BSD-3-Clause

from django.urls import path, include
from django.contrib.auth.views import LoginView
from django.views.generic import TemplateView

from django_latch2.urls import urlpatterns as latch_urls
from django_latch2.decorators import paired_user_required, unpaired_user_required

from .views import (
    RequirePairedUserWithClassDecoratorView,
    RequireUnPairedUserWithMethodDecoratorView,
)

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("accounts/login/", LoginView.as_view(), name="login"),
    path(
        "require-paired-view-instance",
        paired_user_required(
            TemplateView.as_view(template_name="django_latch2/require_paired_user.html")
        ),
        name="require_paired_view_instance",
    ),
    path(
        "require-unpaired-view-instance",
        unpaired_user_required(
            TemplateView.as_view(
                template_name="django_latch2/require_unpaired_user.html"
            )
        ),
        name="require_unpaired_view_instance",
    ),
    path(
        "require-paired-view-class",
        RequirePairedUserWithClassDecoratorView.as_view(),
        name="require_paired_view_class",
    ),
    path(
        "require-unpaired-view-class",
        RequireUnPairedUserWithMethodDecoratorView.as_view(),
        name="require_unpaired_view_class",
    ),
]

urlpatterns += latch_urls
