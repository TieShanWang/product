# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class ProductMeasureUnit(models.Model):

    class Meta:

        verbose_name = '计量方式'

        verbose_name_plural = '计量方式'

    code = models.CharField(max_length=20, verbose_name='计量方式')

    name = models.CharField(max_length=20, verbose_name='计量方式名称')

    def toJson(self):
        return {
            'code' : self.code,
            'name' : self.name,
            'id' : '%d' % self.id,
        }

    def __str__(self):
        return '%s-%s' % (self.name, self.code)