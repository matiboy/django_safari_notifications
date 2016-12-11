=============================
django_safari_notifications
=============================

.. image:: https://badge.fury.io/py/django-safari-notifications.png
    :target: https://badge.fury.io/py/django-safari-notifications

.. image:: https://travis-ci.org/matiboy/django-safari-notifications.png?branch=master
    :target: https://travis-ci.org/matiboy/django-safari-notifications

Support for Safari Push Notifications from within Django

Documentation
-------------

The full documentation is at https://django-safari-notifications.readthedocs.io.

For the Safari Push documentations, refer to `Apple Safari Push`_.

Quickstart
----------

Install django_safari_notifications::

    pip install django-safari-notifications

If you already have a valid "pushPackage.zip", please serve it directly via your web server (Nginx/Apache) at the corresponding url: "{webServiceUrl}/{version}/pushPackages/{websitePushID}" (refer to `Apple Safari Push`_)

Else, you *must* subclass `django_safari_notifications.apps.DjangoSafariNotificationsConfig` and set the `cert` and `passphrase` values.

.. code-block:: python

    from django_safari_notifications.apps import DjangoSafariNotificationsConfig

    class MySafariNotificationsConfig(DjangoSafariNotificationsConfig):
        cert = '/path/to/cert.pem'
        passphrase = 'passphrase for key'

then add your config to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'my_safari_app.apps.MySafariNotificationsConfig', # if you need the pushPackage to be dynamically built
        ## OR ##
        'django_safari_notifications.apps.DjangoSafariNotificationsConfig', # If you are serving your own push package via Nginx
        ...
    )

Add django_safari_notifications's URL patterns:

.. code-block:: python

    from django_safari_notifications import urls as django_safari_notifications_urls


    urlpatterns = [
        ...
        url(r'^', include(django_safari_notifications_urls, namespace='safari_pn')),
        ...
    ]

Do not use any prefix for the unless you are serving your own `pushPackage.zip` statically

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage


.. _`Apple Safari Push`: https://developer.apple.com/library/content/documentation/NetworkingInternet/Conceptual/NotificationProgrammingGuideForWebsites/PushNotifications/PushNotifications.html#//apple_ref/doc/uid/TP40013225-CH3-SW7
