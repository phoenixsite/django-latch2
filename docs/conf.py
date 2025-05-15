"""
Configuration file for the documentation.
"""

import sys
import os
from importlib.metadata import version as get_version

import django
from django.conf import settings

settings.configure(
    INSTALLED_APPS=[
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django_latch2",
    ],
    DEBUG=True,
)

django.setup()

project = "django-latch2"
copyright = "Carlos Romero Cruz and contributors"
author = "Carlos Romero Cruz"
version = get_version("django_latch2")
release = version
extensions = [
    "sphinx.ext.autodoc",
    "notfound.extension",
    "sphinx.ext.intersphinx",
    "sphinx_copybutton",
    "sphinxext.opengraph",
    "sphinx.ext.viewcode",
    "sphinx_inline_tabs",
    "sphinxcontrib_django",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"

intersphinx_mapping = {
    "django": (
        "https://docs.djangoproject.com/en/stable/",
        "https://docs.djangoproject.com/en/stable/_objects/",
    ),
    "python": ("https://docs.python.org/3", None),
    "requests": ("https://requests.readthedocs.io/en/stable/", None),
}

# Spelling check needs an additional module that is not installed by default.
# Add it only if spelling check is requested so docs can be generated without it.
if "spelling" in sys.argv:
    extensions.append("sphinxcontrib.spelling")

# Spelling language.
spelling_lang = "en_US"

# Location of word list.
spelling_word_list_filename = "spelling_wordlist.txt"

# The documentation does not include contributor names, so we skip this because it's
# flaky about needing to scan commit history.
spelling_ignore_contributor_names = False

# OGP metadata configuration.
ogp_enable_meta_description = True
ogp_site_url = "https://django-latch2.readthedocs.io/"

# Django settings for sphinxcontrib-django.
sys.path.insert(0, os.path.abspath("."))
django_settings = "docs_settings"

locale_dirs = ["locale/"]  # path is example but recommended.
gettext_compact = False  # optional.
