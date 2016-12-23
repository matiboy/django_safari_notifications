# -*- coding: utf-8 -*-
from django.db import models
from model_utils import Choices
from model_utils.models import StatusModel


ICON_SIZES = ['16x16', '16x16@2x', '32x32', '32x32@2x', '128x128', '128x128@2x']


class Domain(models.Model):
    name = models.CharField(max_length=255)
    website_push_id = models.CharField(max_length=255)
    url_format_string = models.CharField(max_length=255)
    web_service_url = models.CharField(max_length=255)


class DomainNames(models.Model):
    domain = models.ForeignKey(Domain, related_name='names')
    name = models.URLField(max_length=255, db_index=True)


class Token(StatusModel):
    STATUS = Choices('granted', 'denied')
    token = models.CharField(max_length=180, unique=True)
    website_push_id = models.CharField(max_length=255, default='')
    domain = models.ForeignKey(Domain, null=True, related_name='tokens')

    def __str__(self):
        return '{} ({})'.format(self.token, self.status)

def validate_website_push_id(s):
    return s.startswith('web.')
