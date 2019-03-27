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

Configure app urls

```python
    from django.urls import path, include

    urlpatterns = [
        [...]
        path('latch/', include('latch.urls'))
        [...]
    ]
```

Then apply migrations

    $ python manage.py makemigrations


TO-DO:
* Configuring Latch API via environment variables.


# Bugs and requests

Please report any bug/issue or feature request in GitHub's issue tracker.

https://github.com/javimoral/django-latch/issues

# License

You can use this module under Apache 2.0 license. See LICENSE file for details.

latch-sdk-python is published under GNU General Public License 2.0. Rights belongs to ElevenPaths, more information and updated versionas at:
https://github.com/ElevenPaths/latch-sdk-python

# Authors

Originaly developed by Javier Olascoaga and [RootedCON](http://rootedcon.com/).
