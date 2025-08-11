.. _view-access:
.. module:: django_latch.mixins

View access control
===================

There may be some views that shouldn't be accessed by users who haven't
configured their latch yet, and vice versa. That is the reason ``django-latch``
provides mixins for class-based views and decorators for function-based views.

An example of views limited to users with a paired or unpaired latch are
:class:`~django_latch.views.PairLatchView` and
:class:`~django_latch.views.UnpairLatchView`.

Mixins
------

``django-latch`` offers two class-based view `mixins
<https://docs.djangoproject.com/en/5.2/topics/auth/default/#redirecting-unauthorized-requests-in-class-based-views>`_
to limit the access to some views according to the fact that a user has or
hasn't configured its latch.

.. autoclass:: PairedUserRequiredMixin

.. autoclass:: UnpairedUserRequiredMixin


Decorators
----------

.. module:: django_latch.decorators


``django-latch`` provides two `decorators <https://docs.djangoproject.com/en/5.2/topics/http/decorators/>`_
that can be applied to views.

.. autofunction:: paired_user_required

.. autofunction:: unpaired_user_required
