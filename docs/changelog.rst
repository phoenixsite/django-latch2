.. _changelog:

Changelog
=========

Version 5.2.0
-------------

Released on .

This new version most likely have breaking changes.

* Adopted `DjangoVer <https://www.b-list.org/weblog/2024/nov/18/djangover/>`_ as version scheme.
* Changed license from Apache License 2.0 to BSD-3-Clause.

**Version support:**

* ``django-latch2`` now supports Django 4.2, 5.1 and 5.2. See
  `Django's Python support matrix <https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-can-i-use-with-django>`_
  for details of which Python versions are compatible with each version of
  Django.
* Support for Latch API version 2 via the `latch_sdk_python <https://github.com/Telefonica/latch-sdk-python>`_.

**New features:**

* Added checks for the `Django's check command <https://docs.djangoproject.com/en/5.2/topics/checks/>`_.
* Added :func:`django_latch2.decorators.unpaired_user_required` view decorator.
* Added :class:`django_latch2.mixins.UnpairedUserRequiredMixin` and :class:`django_latch2.mixins.PairedUserRequiredMixin`
  class-based views mixins.
* Added authentication backend mixin :class:`django_latch2.backends.LatchModelBackendMixin`.

**Changes:**

* ``latch.views.latch_is_configured`` view decorator is now :func:`django_latch2.decorators.paired_user_required`.
* ``latch.views.pair`` function-based view is now :class:`django_latch2.views.PairLatchView` class-based view.
* ``latch.views.unpair`` function-based view is now :class:`django_latch2.views.UnpairLatchView` class-based view.
* Removed ``latch.models.UserProfile``. Now the user's account id is in :class:`django_latch2.models.LatchUserConfig`.
* The test suite was restructured.
* The included URLconf now has URLs to inform success on pairing and unpairing operations.
* The default authentication backend with Latch support (previously ``latch.auth_backend.LatchAuthBackend``,
  now :class:`django_latch2.backends.LatchDefaultModelBackend`) now inherit directly from :class:`~django.contrib.auth.backends.ModelBackend`.
* ``latch.forms.LatchPairForm`` is now :class:`django_latch2.forms.PairLatchForm`.

**Removals:**

* Removed ``latch.models.LatchSetup``.
* Removed the latch status view (``latch.views.status``).
* Removed the unpairing form (``latch.forms.LatchUnpairForm``).

Version 0.3
-----------

Released on 31 March 2019.

Version 0.2.1
-------------

Released on 30 March 2019.

Version 0.2
-----------

Released on 28 March 2019.
