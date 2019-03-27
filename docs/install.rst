.. _install:

Installation
============

Currently, we support

* >= Django 2.0
* >= Python 3.5

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

Authentication mechanism
########################

Latch doesn't care about the authentication mechanism, just stops authentication process raising a
`PermissionDeniedException <https://docs.djangoproject.com/en/2.1/ref/exceptions/#permissiondenied>`_ when the account is locked.

Your application must rely on another authentication backends, putting :code:`LatchAuthBackend` first in the list.

.. warning:: **Timing attacks**

    Currently, when an user has Latch configured and blocking login attempts
    the password hashing doesn't run, thus, making possible to extract pairing
    status information about the users.

Bypass when service is unreachable
##################################

:code:`LATCH_BYPASS_WHEN_UNREACHABLE` controls the behaviour when Latch service is unavailable.

- If left unconfigured or set to :code:`True` login attempts of paired accounts will be granted permission when connections with Latch service fails.
- If set to :code:`False` login attempts of paired accounts will be denied when connections with Latch service fails.

Configuring API credentials
###########################

Once the app is installed and the migrations are applied, create a new object based on the :class:`LatchStatus` model.

.. note::
    :class:`LatchStatus` register itself in the admin panel, if you prefer configure the API that way.

