# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .model_measureUnit import ProductMeasureUnit

from django.db.models.signals import post_save

from django.dispatch import receiver

from mysite.settings import MEDIA_ROOT_SF

import os, shutil

# 产品分类
class ProductCategory(models.Model):

    class Meta:

        verbose_name = '商品分类'

        verbose_name_plural = '商品分类'

    code = models.CharField(max_length=20,
                            verbose_name='商品类别（英文）')

    name = models.CharField(max_length=20,
                            verbose_name='商品类别（中文）')

    def __str__(self):
        return '%s-%s' % (self.name, self.code)

    def toJson(self):
        return {
            'code' : self.code,
            'name' : self.name,
            'id' : '%d' % self.id,
        }

class Product(models.Model):

    class Meta:

        verbose_name = '商品列表'

        verbose_name_plural = '商品列表'

    # active = models.BooleanField(default=True,)

    # 名称
    name_en = models.CharField(max_length=50,
                               verbose_name='中文名称',)

    name_en_py = models.CharField(max_length=100,
                                  verbose_name='拼音')

    alias_num = models.IntegerField(verbose_name='数字编号',)

    alias_en = models.CharField(max_length=10,
                                verbose_name='英文编码',)

    # 头像
    icon = models.URLField(max_length=100,
                            null=True,
                            verbose_name='头像',
                            blank=True,)

    # 码
    sid = models.CharField(max_length=100,
                           verbose_name='条形码',)

    qrid = models.CharField(max_length=100,
                           verbose_name='二维码',)

    # 价格
    price_base = models.FloatField(verbose_name='进价', default=0.00,)

    price_sale = models.FloatField(verbose_name='售价',)

    # 商品分类
    p_catg = models.ForeignKey(ProductCategory, related_name='product_category', null=True, on_delete=models.SET_NULL, verbose_name='商品分类',)

    # 计量方式
    measure_unit = models.ForeignKey(ProductMeasureUnit, related_name='product_measure_unit', verbose_name='计量方式',)

    # 备注
    desc = models.CharField(max_length=200, verbose_name='备注', default='')

    def toJson(self):
        return {
            'name_en' : self.name_en,
            'name_en_py' : self.name_en_py,
            'alias_num' : '%d' % self.alias_num,
            'alias_en' : self.alias_en,
            'icon' : self.icon,
            'sid' : self.sid,
            'qrid' : self.qrid,
            'price_base' : '%.2f' % self.price_base,
            'price_sale' : '%.2f' % self.price_sale,
            'p_catg' : self.p_catg.toJson(),
            'measure_unit' : self.measure_unit.toJson(),
            'desc' : self.desc,
        }

    def __str__(self):
        return '%s-%s' % (self.sid, self.name_en)
