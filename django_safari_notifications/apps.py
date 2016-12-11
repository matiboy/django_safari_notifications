# -*- coding: utf-8
from django.apps import AppConfig
import logging

class DjangoSafariNotificationsConfig(AppConfig):
    name = 'django_safari_notifications'
    verbose_name = 'Safari Push Notifications'
    version = 'v1'
    service_base = 'push'
    logger = logging.getLogger('django_safari_notifications')
    # Provide path to a pem file containing the certificate, the key as well as Apple's WWDRCA
    cert = 'path/to/your/cert'
    passphrase = ''
    # [OPTIONAL] Set the path to the push package if you've already created and signed it properly
    push_package = None
