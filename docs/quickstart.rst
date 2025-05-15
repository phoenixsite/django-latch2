.. _quickstart:

Quick start
===========

First, you'll need to install django-latch2. If you haven't already done it,
see :ref:`the installation options <install>`.

.. _obtain_credentials:

Obtain Latch credentials
------------------------

Then, the next steps consist on getting the required parameters to connect
to Latch: an application identifier and a secret key. For that, you need
to sign up on the `Latch Developer Portal <https://latch.tu.com/www/signup>`_ or
take on their services. Follow the instructions on the My Applications dashboard
to create a new application and obtain the credentials.

Configure the required settings
-------------------------------

Once you have the Latch application's credentials, you'll need to
configure your Django project. The modifications on your `settings module
<https://docs.djangoproject.com/en/5.2/topics/settings/>`_ are:

1. Add ``"django_latch2"`` to the :data:`~django.conf.settings.INSTALLED_APPS` list.
2. Include the settings ``LATCH_APP_ID`` and ``LATCH_SECRET_KEY``.
3. Add a subclass of :class:`~django_latch2.backends.LatchModelBackendMixin` to the :data:`~django:conf.settings.AUTHENTICATION_BACKENDS` list.

Apart from these changes on the `settings module <https://docs.djangoproject.com/en/5.2/topics/settings/>`_,
you also have to :ref:`create some templates <create-templates>` and :ref:`set up some
URLs <set-up-urls>`.

Latch credentials
~~~~~~~~~~~~~~~~~

In order to connect the Django application to the Latch API, ``django-latch2``
need the two parameters obtained in the :ref:`step for creating an application in
the Latch site <obtain_credentials>`; that is, the application id and its secret
key. ``django-latch2`` get these settings from the `settings module <https://docs.djangoproject.com/en/5.2/topics/settings/>`_
from the attributes ``LATCH_APP_ID`` and ``LATCH_SECRET_KEY``.

To set these two parameters, I recommend you using environment variables or a remote
credential service, like `HashiCorp Vault <https://www.hashicorp.com/es/products/vault>`_
or any other from some cloud provider (no, they haven't paid me anything).

For example, to set these parameters using environment variables you need first to the session
where the application will run

.. tab:: Unix-based

    .. code-block:: shell

        export LATCH_APP_ID = "<your-app-id>"
        export LATCH_APP_SECRET = "<you-app-secret>"

.. tab:: Windows

    .. code-block:: powershell

        $env:LATCH_APP_ID = "<your-app-id>"
        $env:LATCH_APP_SECRET = "<you-app-secret>"

or, even better, write those in an `.env file <https://www.dotenv.org/docs/security/env.html>`_
, which should have those permissions to be read only by the OS user who will run the
`web server <https://docs.djangoproject.com/en/5.2/howto/deployment/#how-to-deploy-django>`_
(or the `run_server command <https://docs.djangoproject.com/en/5.2/ref/django-admin/#django-admin-runserver>`_,
in case of still developing the application):

.. code-block::

    LATCH_APP_ID=<your-app-id>
    LATCH_APP_SECRET=<you-app-secret>

To load those values from the .env file, you also need to install the
`python-dotenv package <https://pypi.org/project/python-dotenv/>`_:

.. tab:: Unix-based

    .. code-block:: shell

        python -m pip install python-dotenv

.. tab:: Windows

    .. code-block:: shell

        py -m pip install python-dotenv

Then, you just need to get those variables from add to your setting module:

.. code-block:: python

        # Beginning of the settings.py module
        from dotenv import load_dotenv
        load_dotenv("<name-of-your-.env-file")
        ...
        LATCH_APP_ID = os.getenv("LATCH_APP_ID")
        LATCH_APP_SECRET = os.getenv("LATCH_APP_SECRET")

For more information about security during the development and deployment of a Django application, I
recommend reading the `security section of the Django documentation <https://docs.djangoproject.com/en/5.2/topics/security/>`_
You would have committed a war crime if you haven't already done it. (really, just read it).

Setting up the authentication backend
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Now, in order to let Latch block or allow the access to your users, you need to
modify your authentication backends.

If you are using the `Django's default authentication process <https://docs.djangoproject.com/en/5.2/topics/auth/default/>`_,
then you must substitute, or add if it is not specified in your settings module, the :class:`~django.contrib.auth.backends.ModelBackend`
for :class:`~django_latch2.backends.LatchDefaultModelBackend`:

.. code-block:: python

    AUTHENTICATION_BACKENDS = ["django_latch2.backends.LatchDefaultModelBackend"]

if you have implemented a custom authentication process which uses a different authentication backend,
you can also add to it the Latch check by creating an inherited class from the :class:`~django_latch2.backends.LatchModelBackendMixin`
and your custom backend:

.. code-block:: python

    from django.contrib.auth.backends import BaseBackend

    from django_latch2.backend.LatchModelBackendMixin

    # Your custom backend
    class YourCustomAuthBackend(BaseBackend):
        ...

    class LatchYourCustomAuthBackend(LatchModelBackendMixin, YourCustomBackend):
        pass

or simply by inheriting directly from :class:`~django_latch2.backends.LatchModelBackendMixin`:

.. code-block:: python

    from django.contrib.auth.backends import BaseBackend

    from django_latch2.backend.LatchModelBackendMixin

    # Your custom backend
    class LatchYourCustomAuthBackend(LatchModelBackendMixin, BaseBackend):
        ...

Then, it must be added to your settings module:

.. code-block:: python

    AUTHENTICATION_BACKENDS = ["path.to.your.backends.LatchYourCustomAuthBackend"]


.. important:: **Using more than one authentication backend**

    In order to block or allow all the requested attempts from authenticated users, the authentication backend
    that is subclass of :class:`~django_latch2.backends.LatchModelBackendMixin` must be the first one
    in the :data:`AUTHENTICATION_BACKENDS` list.

In case your are using a `remote authentication service <https://docs.djangoproject.com/en/5.2/howto/auth-remote-user/>`_
you will have to implement the Latch access from that remote service.

Check the :ref:`authentication backends section <authentication-backends>` for a more detailed information
about using backends.

.. _set-up-urls:

Setting up URLs
---------------

``django-latch2`` includes a Django URLconf that sets up URL patterns for
the :ref:`required views <views>`. For example, the URLs can be placed under
the prefix ``/accounts/`` by adding the following to your project's root
URLconf:

.. code-block:: python

    from django.urls import include, path

    urlpatterns = [
        ...
        path("accounts/", include("django_latch2.urls")),
        ...
    ]

Then, authenticated users would be able to pair or unpair their
latch by visiting the URLs ``/accounts/pair-latch/`` and
``/accounts/unpair-latch/``.

The following `URL names <https://docs.djangoproject.com/en/5.2/topics/http/urls/#reverse-resolution-of-urls>`_
are defined in ``django_latch2.urls``:

* ``django_latch2_pair`` is the view for pairing the authenticated user's latch.
* ``django_latch2_pair_complete`` is the post-pairing success view.
* ``django_latch2_unpair`` is the view for unpairing the authenticated user's latch.
* ``django_latch2_unpair_complete`` is the post-unpairing success view.

.. _create-templates:

Create the required templates
-----------------------------

Lastly, you also need to create some templates required by the ``django-latch2`` views.
The required templates are the following:

``django_latch2/pair_account_form.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used to show the pairing form. It has the following context:

``form``
    The pairing form. It asks the user for the Latch token
    generated on the Latch mobile app.


``django_latch2/pair_complete.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used after successfully paired the authenticated user with the Latch service.
It should inform the user that it can now block or allow the access to the
Django application by using the Latch mobile app.

``django_latch2/unpair_account.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used to ask the user for confirming that it really wants to unpair its latch. It has
the following context:

``unpair_error``
    If the user confirmed the unpairing via HTTP ``POST`` but the unpairing operation
    failed in the Latch service, this variable will be present and will contain
    a :class:`dict` with information about the error: a message (``message``), an error code
    (``code``) and extra parameters (``params``).

``django_latch2/unpair_complete.html``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Used after successfully unpaired the authenticated user with Latch. It should
inform the user that it can no longer block or allow the access to the Django
application by using the Latch mobile app.
