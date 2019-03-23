django-latch
============

Django and Latch integration

Installation
-------------

To install it, simply: ::
   
    git clone https://github.com/javimoral/django-latch.git
    cd django-latch
    python setup.py install



Requirements
------------

- Python > 3.5
- Django >= 2.0



Configuration
-------------

- TO-DO


In your ``settings.py`` file you need to add the following directives:

```python

   INSTALLED_APPS = (
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'latch',
    )

    # Add auth profile 
    AUTH_PROFILE_MODULE='latch.UserProfile'
    
    # Add the authentication backend
    AUTHENTICATION_BACKENDS = (
            'latch.auth_backend.LatchAuthBackend',
    )
```
    
TODO
----

* Add a signal when deleting a user to remove the profile
* Add the UserProfile management to the admin


Bugs and requests
-----------------

Please report any bug/issue or feature request in GitHub's issue tracker.

https://github.com/javimoral/django-latch/issues


License
-------

You can use this module under Apache 2.0 license. See LICENSE file for details.

The rights for latch/latch.py belongs to ElevenPaths, more information and updated versionas at:
https://github.com/ElevenPaths/latch-sdk-python

Author
------

Originaly developed by Javier Olascoaga and RootedCON

