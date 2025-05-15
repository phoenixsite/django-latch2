.. _settings:
.. module:: django.conf.settings

Settings
========

In order to start using ``django-latch2`` in your Django project, you need
to set up some settings in your `settings module <https://docs.djangoproject.com/en/5.2/topics/settings/>`_.
Other settings are optional and their default value may be enough for your
needs, but it is also recommended reading what those are about.

Required settings
-----------------

.. data:: LATCH_APP_ID

    Identifier of the application in `Latch <https://latch.tu.com/>`_. You
    need to register as a developer in the Latch portal to get this id and
    the :data:`LATCH_SECRET_KEY`.

    The value of this setting needs to be kept secret, so it is recommended
    using a secret manager or environment variables.

.. data:: LATCH_SECRET_KEY

    Secret key of the application in `Latch <https://latch.tu.com/>`_. You
    need to register as a developer in the Latch portal to get this secret and
    the :data:`LATCH_APP_KEY`.

    The value of this setting needs to be kept secret, so it is recommended
    using a secret manager or environment variables.

Optional settings
-----------------

.. data:: LATCH_HTTP_BACKEND

    A :class:`str` that indicates the HTTP backend to use to interact
    with the Latch service. This is used by the
    `latch_sdk_python <https://github.com/Telefonica/latch-sdk-python>`_,
    package.

    A default of ``'http'`` is assumed when this setting is not supplied. This
    value implies that `latch_sdk_python <https://github.com/Telefonica/latch-sdk-python>`_
    will use the :class:`http.client.HTTPConnection`  and
    :class:`http.client.HTTPSConnection` from the standard library to manage the
    requests and responses to and from the Latch service. If the
    value supplied is ``'requests'`` or ``'httpx'``, the corresponding packages
    have to be installed. In case of the ``'requests'`` option, this can be done
    by running the command:

    .. tab:: Unix-based

        .. code-block:: shell

            python -m pip install django-latch2[requests]

    .. tab:: Windows

        .. code-block:: shell

            py -m pip install django-latch2[requests]


    Then, `latch_sdk_python <https://github.com/Telefonica/latch-sdk-python>`_
    will use :class:`requests.Session`.

    or in case of the ``'httpx'`` option:

    .. tab:: Unix-based

        .. code-block:: shell

            python -m pip install django-latch2[httpx]

    .. tab:: Windows

        .. code-block:: shell

            py -m pip install django-latch2[httpx]

    Then, `latch_sdk_python <https://github.com/Telefonica/latch-sdk-python>`_
    will use `httpx.Client <https://www.python-httpx.org/api/#client>`.
