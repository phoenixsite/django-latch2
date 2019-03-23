# From C. Trudeau on Stack Overflow
# https://stackoverflow.com/questions/30656162/migrations-in-stand-alone-django-app
import django

from django.conf import settings
from django.core.management import call_command

settings.configure(
    DEBUG=True,
    INSTALLED_APPS=("django.contrib.contenttypes", "django.contrib.auth", "latch"),
)

django.setup()
call_command("makemigrations", "latch")
