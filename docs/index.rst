django-latch
==================================

django-latch provides integration with `Latch <https://latch.elevenpaths.com/>`_
service by `ElevenPaths <https://www.elevenpaths.com/>`_, adding an aditional layer of security to the authentication process.

Currently, we support

* Python 3.4, 3.5, 3.6, 3.7
* Django 2.0, 2.1, 2.2, 3.0

This package doesn't give an authentication method by itself, just modify the authentication
flow stoping it if the user has decided to lock in his account. You must rely on another
authentication method like Django default :code:`ModelBackend`.

Originaly developed by Javier Olascoaga and `RootedCON <http://rootedcon.com/>`_


Documentation contents
----------------------

.. toctree::
   :maxdepth: 1

   install
   usage

