# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

class MeasureUnit(models.Model):

    class Meta:

        verbose_name = '计量方式'

        verbose_name_plural = '计量方式'

    code = models.CharField(max_length=20, verbose_name='计量方式')

    name = models.CharField(max_length=20, verbose_name='计量方式名称')

    def __str__(self):
        return self.code + '--' + self.name

def getUnitByType(code):
    return MeasureUnit.objects.filter(code=type)

# 序列化为 code name 列表
_serial = None
def serial():
    return _serial or [{'code': obj.code, 'name': obj.name} for obj in MeasureUnit.objects.all()]

# 清除序列缓存
def clear_serial_cache():
    _serial = None

