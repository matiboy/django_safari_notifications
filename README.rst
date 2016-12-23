================================
Django Safari Push Notifications
================================

.. image:: https://img.shields.io/pypi/v/django-safari-notifications.svg
    :target: https://pypi.python.org/pypi/django-safari-notifications
    :alt: Latest PyPI version

.. image:: https://travis-ci.org/matiboy/django_safari_notifications.png?branch=master
    :target: https://travis-ci.org/matiboy/django_safari_notifications

Support for Safari Push Notifications from within Django. Note that this package helps *registering* notifications, not sending them. Safari Push works with APNs, so for sending, please use `APNs Clerk`_.

Documentation
-------------

The full documentation will soon be at https://django-safari-notifications.readthedocs.io.

For the Safari Push documentations, refer to `Apple Safari Push`_.

Quickstart
----------

Install django_safari_notifications::

    pip install django-safari-notifications

If you already have a valid :code:`pushPackage.zip`, please serve it directly via your web server (Nginx/Apache) at the corresponding url: :code:`{webServiceUrl}/{version}/pushPackages/{websitePushID}` (refer to `Apple Safari Push`_)

Else, you *must* subclass :code:`django_safari_notifications.apps.DjangoSafariNotificationsConfig` and set the :code:`cert` and :code:`passphrase` values.

.. code-block:: python

    from django_safari_notifications.apps import DjangoSafariNotificationsConfig

    class MySafariNotificationsConfig(DjangoSafariNotificationsConfig):
        cert = '/path/to/cert.pem'
        passphrase = 'passphrase for key'

then add your config to your :code:`INSTALLED_APPS`:

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

Do not use any prefix for the urls, unless you are serving your own :code:`pushPackage.zip` statically

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

.. _`APNs Clerk`: https://pypi.python.org/pypi/apns-clerk/0.2.0
