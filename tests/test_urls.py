#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-safari-notifications
------------

Tests for `django-safari-notifications` urls module.
"""

from django.test import TestCase

from django.apps import apps
import random
import string
import mock
import json
import sys
from django.conf import settings
from importlib import import_module
try:
    import importlib
    importlib.reload
except AttributeError:
    import imp as importlib

from django.test.utils import override_settings


class TestDefaultUrls(TestCase):
    def test_default_log_path(self):
        response = self.client.post(
            '/push/v1/log',
            content_type='application/json',
            data=json.dumps({'logs': []})
        )
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        pass

class TestUrls(TestCase):
    # Override settings though with same value, forces a refresh
    @override_settings(ROOT_URLCONF="django_safari_notifications.urls")
    def setUp(self):
        config = apps.get_app_config('django_safari_notifications')
        self.path = ''.join(random.choice(string.ascii_lowercase) for _ in range(8))
        config.service_base = self.path
        # Force reload urls
        importlib.reload(sys.modules[settings.ROOT_URLCONF])

    def test_log_path(self):
        response = self.client.post(
            '/%s/v1/log' % self.path,
            content_type='application/json',
            data=json.dumps({'logs': []})
        )
        self.assertEqual(response.status_code, 200)

    def test_disallowed_methods(self):
        for method in ('get', 'delete', 'put'):
            response = getattr(self.client, method)(
                '/%s/v1/log' % self.path
            )
            self.assertEqual(response.status_code, 405)

    def tearDown(self):
        pass
