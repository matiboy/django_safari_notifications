# -*- coding: utf-8 -*-
from django.views.generic import View
from django.apps import apps
from django.http import HttpResponse
import json
config = apps.get_app_config('django_safari_notifications')
logger = config.logger

CONTENT_TYPE = 'application/zip'


class Log(View):
    def post(self, request):
        post = json.loads(request.body.decode('utf-8'))
        for log in post['logs']:
            logger.error(log)
        return HttpResponse('')


class RegistrationChanges(View):
    """

    """
    def post(self, request, device_token, website_push_id):
        logger.debug('Change in registration for website {pid}: token {token} {post}'.format(
            post=request.POST, token=device_token, pid=website_push_id)
        )
        return HttpResponse('')

    def delete(self, request, device_token, website_push_id):
        logger.debug('Attempt to delete registration for website {pid}: token {token} {post}'.format(
            post=request.POST, token=device_token, pid=website_push_id)
        )
        return HttpResponse('')


class PushPackage(View):
    """
    This view serves the pushPackage.zip as per Apple's requirements
    If push_package is provided in the config, serves that statically. This is the easiest way, but only works if your pushPackage isn't dynamic e.g. user token, different allowed domains etc

    If no push_package, the view generates one
    """
    def post(self, request, website_push_id):
        if config.push_package is not None:
            with open(config.push_package, 'rb') as pp:
                return HttpResponse(pp, content_type=CONTENT_TYPE)
