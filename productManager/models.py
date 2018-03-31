# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from .MeasureUnit import *

from django.db.models.signals import post_save

from django.dispatch import receiver

from mysite.settings import MEDIA_ROOT_SF

import os, shutil

def android_tutu_upload(a, b):
    return 'tutulive_android_andoir.apk'

class AndroidTuTUModel(models.Model):

    class Meta:

        verbose_name = '安卓兔兔直播包'

        verbose_name_plural = '安卓兔兔直播包'

    path = models.FileField(verbose_name='路径')

@receiver(post_save, sender=AndroidTuTUModel)
def androidtutumodel_after(**kwargs):
    instance = kwargs['instance']
    p = MEDIA_ROOT_SF + '/android.apk'
    if (os.path.exists(p)):
        os.remove(p)
    shutil.copyfile(instance.path.path, p)

def ios_tutu_upload(a, b):
    return 'tutulive_ios_ios.ipa'

class IOSTuTUModel(models.Model):

    class Meta:

        verbose_name = 'iOS兔兔直播包'

        verbose_name_plural = 'iOS兔兔直播包'

    path = models.FileField(verbose_name='路径')

@receiver(post_save, sender=IOSTuTUModel)
def iostutumodel_after(**kwargs):
    instance = kwargs['instance']
    p = MEDIA_ROOT_SF + '/meilibo.ipa'
    if (os.path.exists(p)):
        os.remove(p)
    shutil.copyfile(instance.path.path, p)


# 产品分类
class ProductCategory(models.Model):

    class Meta:

        verbose_name = '商品分类'

        verbose_name_plural = '商品分类'

    type = models.CharField(max_length=20,
                            verbose_name='商品类别（英文）')

    name = models.CharField(max_length=20,
                            verbose_name='商品类别（中文）')


class Product(models.Model):

    class Meta:

        verbose_name = '商品列表'

        verbose_name_plural = '商品列表'

    # 名称
    name_en = models.CharField(max_length=50,
                               verbose_name='中文名称',)

    name_en_py = models.CharField(max_length=100,
                                  verbose_name='拼音')

    alias_num = models.IntegerField(verbose_name='数字编号',)

    alias_en = models.CharField(max_length=10,
                                verbose_name='英文编码',)

    # 价格
    price_base = models.FloatField(verbose_name='进价', default=0.00,)

    price_sale = models.FloatField(verbose_name='售价',)


    # 日期
    date_birth = models.DateField(verbose_name='生产日期', null=True,)

    date_end = models.DateField(verbose_name='过期日期', null=True, )

    date_end_alert = models.IntegerField(verbose_name='过期提醒', null=True,)


    # 备注
    desc = models.CharField(max_length=200, verbose_name='备注', default='')


    # 激活状态
    active = models.BooleanField(default=False,
                                 verbose_name='上架')

    active_time = models.DateTimeField(verbose_name='上架时间')

    disactive_time = models.DateTimeField(blank=True,
                                          null=True,
                                          verbose_name='下架时间')

    # 头像
    icon = models.CharField(max_length=100,
                            null=True,
                            verbose_name='头像',
                            blank=True,)

    # 码
    sid = models.CharField(max_length=100,
                           blank=True,
                           null=True,
                           verbose_name='条形码',)

    qrid = models.CharField(max_length=100,
                           blank=True,
                           null=True,
                           verbose_name='二维码',)

    # 商品分类
    p_catg = models.ForeignKey(ProductCategory, related_name='product_category', null=True, on_delete=models.SET_NULL, verbose_name='商品分类',)

    # 计量方式
    measure_unit = models.ForeignKey(MeasureUnit, related_name='product_measure_unit', verbose_name='计量方式',)

