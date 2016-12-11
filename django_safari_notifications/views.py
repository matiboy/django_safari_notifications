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


config = apps.get_app_config('django_safari_notifications')
logger = config.logger

CONTENT_TYPE = 'application/zip'
ICON_SIZES = ['16x16', '16x16@2x', '32x32', '32x32@2x', '128x128', '128x128@2x']

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
    """ During DEV only, get rid of it later """
    def get(self, request, website_push_id):
        resp = self.post(request, website_push_id)
        resp['Content-Disposition'] = 'attachment; filename=yellow.zip'

        return resp


    """
    This view serves the pushPackage.zip as per Apple's requirements
    If no push_package, the view generates one
    """
    def post(self, request, website_push_id):
        # are we using the Domain models?
        if config.website_conf is not None:
            website_conf = json.dumps(config.website_conf)
            iconset_folder = config.iconset_folder
        else:
            # TODO Read from Domain
            pass

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
            # Therefore, we need to delete the temp file
            os.remove(path)

            with tempfile.NamedTemporaryFile() as signature:
                cmd = ['openssl', 'cms', '-sign', '-signer', config.cert, '-binary', '-in', path, '-outform', 'der', '-out', signature.name, '-passin', config.passphrase]
                logger.info('Openssl cms command called: %s ' % ' '.join(cmd))
                logger.info(subprocess.check_output(cmd))
                zf.write(signature.name, 'signature')


        return HttpResponse(s.getvalue(), content_type=CONTENT_TYPE)
