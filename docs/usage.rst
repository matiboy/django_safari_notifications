=====
Usage
=====

To use django_safari_notifications in a project, add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_safari_notifications.apps.DjangoSafariNotificationsConfig',
        ...
    )

Add django_safari_notifications's URL patterns:

.. code-block:: python

    from django_safari_notifications import urls as django_safari_notifications_urls


    urlpatterns = [
        ...
        url(r'^', include(django_safari_notifications_urls)),
        ...
    ]
