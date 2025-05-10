"""
Minimal Django settings for testing.
"""

# SPDX-License-Identifier: BSD-3-Clause

import pathlib

from django.utils.crypto import get_random_string

APP_DIR = pathlib.Path(__file__).parents[0]

DEFAULT_AUTO_FIELD = "django.db.models.AutoField"
INSTALLED_APPS = (
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django_latch2",
    "tests",
)
ROOT_URLCONF = "tests.urls"
LOGIN_URL = "login"
DATABASES = {"default": {"ENGINE": "django.db.backends.sqlite3", "NAME": ":memory"}}
MIDDLEWARE = (
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
)
SECRET_KEY = get_random_string(12)
SITE_ID = 1
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [APP_DIR / "templates"],
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.debug",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
AUTHENTICATION_BACKENDS = ["django_latch2.backend.LatchDefaultModelBackend"]
LATCH_APP_ID = "a" * 20
LATCH_SECRET_KEY = "b" * 64
LATCH_HTTP_BACKEND = "http"
