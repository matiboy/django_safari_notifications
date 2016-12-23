# -*- coding: utf-8 -*-
from django.views.generic import View
from django.apps import apps
from django.http import HttpResponse
import json
import zipfile
from io import BytesIO
import hashlib
import tempfile
import subprocess
import os
import uuid
from .models import Token, ICON_SIZES
from .signals import permission_denied, permission_granted, push_package_sent


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
    POST is called by APNs when a user accepts, whereas DELETE is when a user denies
    """
    def post(self, request, device_token, website_push_id):
        logger.info('Change in registration for website {pid}: token {token}'.format(
            token=device_token, pid=website_push_id)
        )

        userinfo = self._get_userinfo(request)

        logger.info('Corresponding auth token %s' % userinfo)
        isnew = False
        try:
            token = Token.objects.get(token=device_token)
        except Token.DoesNotExist:
            token = Token.objects.create(
                token=device_token,
                status=Token.STATUS.granted,
                website_push_id=website_push_id
            )
            isnew = True
        else:
            token.status = Token.STATUS.granted
            token.save()

        # TODO decide whether we should send the model or the string token
        permission_granted.send(
            sender=self.__class__,
            token=device_token, userinfo=userinfo, isnew=isnew
        )
        return HttpResponse('')

    def delete(self, request, device_token, website_push_id):
        logger.info('Attempt to delete registration for website {pid}: token {token}'.format(
            token=device_token, pid=website_push_id)
        )
        userinfo = self._get_userinfo(request)

        logger.info('Corresponding auth token %s' % userinfo)
        try:
            token = Token.objects.get(token=device_token)
        except Token.DoesNotExist:
            logger.error('Token {token} was not registered for website {pid}'.format(
                pid=website_push_id, token=device_token
            ))
        else:
            if token.status == Token.STATUS.denied:
                logger.info('Token {token} was already denied for website {pid}'.format(
                    pid=website_push_id, token=device_token
                ))
            else:
                token.status = Token.STATUS.denied
                token.save()

        permission_denied.send(sender=self.__class__, token=device_token, userinfo=userinfo)

        return HttpResponse('')

    def _get_userinfo(self, request):
        """
            Auth token comes as ApplePushNotifications 123abcd123465465jkljdkglfjdfdsfds <- token that was passed in website.conf
        """
        try:
            authentication_header = request.META['HTTP_AUTHORIZATION']
        except KeyError:
            raise ValueError('All APN registrations calls are expected to contain an authorization header')
        apn, _, userinfo = authentication_header.partition(' ')

        if apn != 'ApplePushNotifications':
            raise ValueError('All APN authentication headers are expected to start with ApplePushNotifications')

        return userinfo


class PushPackage(View):
    def _build_website_conf(self, request):
        """
        Use this to override the way the website conf dictionary is created
        """
        # are we using the Domain models?
        if config.website_conf is not None:
            website_conf = config.website_conf.copy()
            iconset_folder = config.iconset_folder
        else:
            # TODO Read from Domain
            pass

        return website_conf, iconset_folder

    def _get_userinfo(self, request):
        body = json.loads(request.body.decode('utf-8'))
        userinfo = body.get(config.userinfo_key, str(uuid.uuid4()))
        return userinfo

    """
    This view serves the pushPackage.zip as per Apple's requirements
    """
    def post(self, request, website_push_id):
        # Body contains authentication. If not we create one
        website_conf, iconset_folder = self._build_website_conf(request)
        userinfo = self._get_userinfo(request)
        website_conf["authenticationToken"] = userinfo
        logger.info('Push will be authenticated with userinfo %s' % userinfo)

        website_conf = json.dumps(website_conf)

        # Create the zip file in memory
        s = BytesIO()
        with zipfile.ZipFile(s, 'w') as zf:
            # along the way, prepare the manifest
            manifest = {}
            hasher = hashlib.sha1()
            # Add website_conf to it
            zf.writestr('website.json', website_conf)
            hasher.update(website_conf.encode())
            manifest['website.json'] = hasher.hexdigest()

            # Go through the icons
            for size in ICON_SIZES:
                hasher = hashlib.sha1()
                icon_name = 'icon_%s.png' % size
                path = '{base}/{icon_name}'.format(base=iconset_folder, icon_name=icon_name)
                with open(path, 'rb') as icon:
                    data = icon.read()
                    path = 'icon.iconset/%s' % icon_name
                    zf.writestr(path, data)
                    hasher.update(data)
                    manifest[path] = hasher.hexdigest()

            # Write the manifest.json file to a temp file since we'll need to sign it
            with tempfile.NamedTemporaryFile(delete=False) as manifest_json:
                path = manifest_json.name
                data = json.dumps(manifest)
                manifest_json.write(data.encode())

            # Had to close manifest_json first before being able to write it to zip (got 0 bytes otherwise)
            zf.write(path, 'manifest.json')

            with tempfile.NamedTemporaryFile() as signature:
                cmd = ['openssl', 'cms', '-sign', '-signer', config.cert, '-binary', '-in', path, '-outform', 'der', '-out', signature.name, '-passin', config.passphrase]
                logger.info('Openssl cms command called: %s ' % ' '.join(cmd))
                logger.info('Openssl command output: %s ' % subprocess.check_output(cmd))
                zf.write(signature.name, 'signature')

            # Due to close above, we need to delete the temp file ourselves
            os.remove(path)

        push_package_sent.send(sender=self.__class__, userinfo=userinfo)

        return HttpResponse(s.getvalue(), content_type=CONTENT_TYPE)
