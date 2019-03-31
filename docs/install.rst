.. _install:

Installation
============

To install django-latch run::

    $ pip install django-latch

You can install directly from source if you don't want to use PyPI.

To install it this way, simply::

    $ git clone https://github.com/javimoral/django-latch.git
    $ cd django-latch
    $ python setup.py install

Configuration and use
#####################

We use `Django Message Framework <https://docs.djangoproject.com/en/2.1/ref/contrib/messages/>`_
so you must configure your application accordingly.

Then, you must

* Include :code:`latch` in your :code:`INSTALLED_APPS`
* Append :code:`latch.auth_backend.LatchAuthBackend` to :code:`AUTHENTICATION_BACKENDS`
* Configure your API credentials
* Configure :code:`LATCH_BYPASS_WHEN_UNREACHABLE`

.. code-block:: python

   INSTALLED_APPS = (
       [...]
        'latch',
    )

    # Append Latch Auth Backend the first in list
    AUTHENTICATION_BACKENDS = [
        'latch.auth_backend.LatchAuthBackend',
        [...]
    ]

    LATCH_APP_ID = <APP Id>
    LATCH_APP_SECRET = <APP Secret>

    LATCH_BYPASS_WHEN_UNREACHABLE = True # True is the default behaviour. Configure as you need.

Next step, configure your project URLs.

.. code-block:: python

    from django.urls import path, include

    urlpatterns = [
        [...]
        path('latch/', include('latch.urls'))
        [...]
    ]

Last, apply migrations after installing the app::

    $ python manage.py makemigrations

.. warning:: **Upgrading from 0.2**

    The method for configuring Latch API has changed. When upgrading from 0.2 the applied migrations
    will remove the model where API parameters used to be stored. You can get them again from Latch API
    settings page though.


Authentication mechanism
########################

Latch doesn't care about the authentication mechanism, just stops authentication process raising a
`PermissionDeniedException <https://docs.djangoproject.com/en/2.1/ref/exceptions/#permissiondenied>`_ when the account is locked.

Your application must rely on another authentication backends, putting
:code:`LatchAuthBackend` first in the list.

.. note:: **Timing attacks**

    When a locked out paired account trys to connect we run the password hasher
    once to avoid timing attack. If the account doesn't exists, we pass the responsability
    to the next auth backend in chain.

Bypass when service is unreachable
##################################

:code:`LATCH_BYPASS_WHEN_UNREACHABLE` controls the behaviour when Latch service
is unavailable.

- If left unconfigured or set to :code:`True` login attempts of paired accounts will be granted permission when connections with Latch service fails.
- If set to :code:`False` login attempts of paired accounts will be denied when connections with Latch service fails.

Configuring API credentials
###########################

Configure in your :code:`settings.py` as you prefer.

.. note::

    The method for configuring your application sensitive settings will be
    dependant of you deployment type. Usually, the prefered method is to use environment variables.

    .. code-block:: python

        import os

        [...]

        LATCH_APP_ID = os.environ.get('LATCH_APP_ID')
        LATCH_APP_SECRET = os.environ.get('LATCH_APP_SECRET')

