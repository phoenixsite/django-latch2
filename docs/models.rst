.. _models:
.. module:: django_latch2.models

Model classes
=============

In order to be able to associate every user who has configured the latch with
the Latch service and check its status (on or off), ``django-latch2`` has to
store the parameter that uniquely identify a user against the Latch service:
an account id.

Following the `Django's guidelines for extending the User model
<https://docs.djangoproject.com/en/5.2/topics/auth/customizing/#extending-the-existing-user-model>`_
the account id is stored in a separate table from the User one, along with a
foreign key pointing to the respective user.

.. autoclass:: LatchUserConfig
