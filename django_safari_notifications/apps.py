# -*- coding: utf-8
from django.apps import AppConfig
import logging


class DjangoSafariNotificationsConfig(AppConfig):
    name = 'django_safari_notifications'
    verbose_name = 'Safari Push Notifications'
    version = 'v1'
    service_base = 'push'
    userinfo_key = 'userinfo'
    logger = logging.getLogger('django_safari_notifications')
    # Provide path to a pem file containing the certificate, the key as well as Apple's WWDRCA
    cert = 'path/to/your/cert'
    passphrase = 'pass:xxxx' # this will be used with -passin in the openssl command so could be with pass, env etc
    # If single site, just set these values. Otherwise create Domain entries
    website_conf = None
    # sample single site: do not include the authenticationToken
    """
    website_conf = {
        "websiteName": "Bay Airlines",
        "websitePushID": "web.com.example.domain",
        "allowedDomains": ["http://domain.example.com"],
        "urlFormatString": "http://domain.example.com/%@/?flight=%@",
        "webServiceURL": "https://example.com/push"
    }
    """
    iconset_folder = '/path/to/your/iconset'
