# django-latch

[![Build Status](https://travis-ci.com/javimoral/django-latch.svg?branch=master)](https://travis-ci.com/javimoral/django-latch)
[![codecov](https://codecov.io/gh/javimoral/django-latch/branch/master/graph/badge.svg)](https://codecov.io/gh/javimoral/django-latch)

Django and Latch integration. Originaly developed by Javier Olascoaga and [RootedCON](http://rootedcon.com/).

# Requirements

- Python > 3.5
- Django >= 2.0

## Installation

To install it, simply:

    $ git clone https://github.com/javimoral/django-latch.git
    $ cd django-latch
    $ python setup.py install

# Configuration

In your `settings.py` file you need to add the following directives:

```python

   INSTALLED_APPS = (
       [...]
        'latch',
    )

    # Add auth profile
    AUTH_PROFILE_MODULE='latch.UserProfile'

    # Append Latch Auth Backend the first in list
    AUTHENTICATION_BACKENDS = [
        'latch.auth_backend.LatchAuthBackend',
        [...]
    ]

    LATCH_BYPASS_WHEN_UNREACHABLE = True # True is the default behaviour. Configure as you need.
```

Latch doesn't care about the authentication mechanism, just stops authentication process when the account is locked. That's why you must rely on another authentication backends, putting LatchAuthBackend first in the list.

`LATCH_BYPASS_WHEN_UNREACHABLE` controls the behaviour when Latch service is unreachable.

- If left unconfigured or set to `True` login attempts of paired accounts will be granted permission when connections with Latch service fails.
- If set to `False` login attempts of paired accounts will be denied when connections with Latch service fails.

Django-Latch relies on the [message framework](https://docs.djangoproject.com/en/2.1/ref/contrib/messages/) so you must setup your project accordingly.

We create some models in database, so you must apply migrations after installing the app.

    $ python manage.py makemigrations

Like `django.contrib.auth` we extend Django Admin templates, if you want to your design, override the following templates:

    latch
    └── templates
        ├── latch_message.html
        ├── latch_pair.html
        ├── latch_status.html
        └── latch_unpair.html

### Loggers
We log failed API connections using `logger.exception`.

# TODO

- Add a signal when deleting a user to remove the profile
- Add the UserProfile management to the admin
- Add 2FA support

# Bugs and requests

Please report any bug/issue or feature request in GitHub's issue tracker.

https://github.com/javimoral/django-latch/issues

# License

You can use this module under Apache 2.0 license. See LICENSE file for details.

latch-sdk-python is published under GNU General Public License 2.0. Rights belongs to ElevenPaths, more information and updated versionas at:
https://github.com/ElevenPaths/latch-sdk-python

# Authors

Originaly developed by Javier Olascoaga and [RootedCON](http://rootedcon.com/).
