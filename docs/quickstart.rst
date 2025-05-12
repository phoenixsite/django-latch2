.. _quickstart:

Quick start guide
=================

First, you'll need to install django-latch2. If you haven't already done it,
see :ref:`the installation options <install>`.

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

1. Add ``"django-latch2"`` to the :data:`~django.conf.settings.INSTALLED_APPS` list.
2. Include the settings ``LATCH_APP_ID`` and ``LATCH_SECRET_KEY``.
3. Add a subclass of :class:`~django_latch2.backends.LatchModelBackendMixin` to the :data:`~django:conf.settings.AUTHENTICATION_BACKENDS` list.


Apart from these changes on the `settings module <https://docs.djangoproject.com/en/5.2/topics/settings/>`_,
you also have to :ref:`create some templates <create-templates>` and :ref:`set up some
URLs <set-up-urls>`.

Latch credentials
~~~~~~~~~~~~~~~~~

Authentication backends
~~~~~~~~~~~~~~~~~~~~~~~

.. _create-templates:

Create required templates
-------------------------


.. _set-up-urls:

Setting up URLs
---------------
