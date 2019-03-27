.. module:: latch.views
.. _usage:

Usage
=====

Views & Decorators
##################

django-latch exposes the following views:

.. py:function:: pair(request, template_name="latch_pair.html")

    Process the pair form. If the user is alredy paired, redirects to the status view
    and shows a message using Django Message Framework.

    View Name: :code:`latch_pair`

.. py:function:: unpair(request, template_name="latch_unpair.html")

    Process the unpair form. If the user is not paired, redirects to the status view
    and shows a message using Django Message Framework.

    View Name: :code:`latch_unpair`

.. py:function:: status(request, template_name="latch_status.html")

    Show status about installation.
    We load two variables in this view:

    * :code:`accountid` Latch API account ID of the current user, if the account is paired.
    * :code:`account_status` Indicating if the user can login, value :code:`on`, or not, value :code:`off`.

    Also note that retrieving status using the API will count as an login attempt, and the users can receive
    notifications on their devices.

    View Name: :code:`latch_status`
    

Also, it expose a decorator

.. py:function:: latch_is_configured(view)

    If Latch is installed but not configured, decorated views will redirect to :code:`status` instead.


Templates
#########

Like `django.contrib.auth <https://docs.djangoproject.com/en/2.1/topics/auth/>`_ we extend Django Admin templates.
You can override the following templates::

    latch
    └── templates
        ├── latch_pair.html
        ├── latch_status.html
        └── latch_unpair.html

Loggers
#######

We log failed API connections using :code:`logger.exception`.

When :code:`LATCH_BYPASS_WHEN_UNREACHABLE` we register each bypassed login with :code:`info` level.