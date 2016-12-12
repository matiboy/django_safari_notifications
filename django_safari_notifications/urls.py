# -*- coding: utf-8 -*-
from . import views
from django.conf.urls import url
from django.apps import apps
from django.views.decorators.csrf import csrf_exempt
config = apps.get_app_config('django_safari_notifications')


urlpatterns = [
    url(
        regex="^{base}/{version}/pushPackages/(?P<website_push_id>[a-z0-9.]+)$".format(base=config.service_base, version=config.version),
        view=csrf_exempt(views.PushPackage.as_view()),
        name='push_package',
    ),
    url(
        regex="^{base}/{version}/devices/(?P<device_token>[0-9a-fA-F]+)/registrations/(?P<website_push_id>[a-z0-9.]+)$".format(base=config.service_base, version=config.version),
        view=csrf_exempt(views.RegistrationChanges.as_view()),
        name='registration_change',
    ),
    url(
        regex="^{base}/{version}/log$".format(base=config.service_base, version=config.version),
        view=csrf_exempt(views.Log.as_view()),
        name='log',
    ),
]
