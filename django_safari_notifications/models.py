# -*- coding: utf-8 -*-

from django.db import models


class Domain(models.Model):
    name = models.CharField(max_length=255)
    website_push_id = models.CharField(max_length=255)
    url_format_string = models.CharField(max_length=255)
    web_service_url = models.CharField(max_length=255)


class DomainNames(models.Model):
    domain = models.ForeignKey(Domain, related_name='names')
    name = models.CharField(max_length=255, db_index=True)
