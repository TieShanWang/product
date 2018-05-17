# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime

import logging

from django.db import models

logger = logging.getLogger("django")

def mini_icon_path(instance, filename):
    '''
    React Native 包 存储路径
    '''

    # extension
    ext = filename.split('.')[-1]

    # nowtime
    nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # app group name
    app_group_name = instance.product.mobile_application_group
    logger.info("get ReactNative package icon image object in group:" + app_group_name)

    # cache path /group/mini/miniid/icon/time.jpg
    path = '%s/mini/%s/icon/%s.%s' % (app_group_name, instance.product.miniId, nowtime, ext)
    logger.info('save path is %s' % path)

    return path

def mini_package_file_path(instance, filename):
    '''
    React Native 包 存储路径
    '''

    # is ios
    ios = instance.isIOS()

    # platform
    platform = 'ios' if ios else 'android'

    # extension
    ext = filename.split('.')[-1]

    # nowtime
    nowtime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    # app group name
    app_group_name = instance.product.mobile_application_group
    logger.info("get ReactNative package upload file object in group:" + app_group_name)

    # cache path /group/mini/miniid/ios/time.zip
    path = '%s/mini/%s/%s/%s.%s' % (app_group_name, instance.product.miniId, platform, nowtime, ext)
    logger.info('save path is %s' % path)

    return path

# 小程序模型
class MiniModel(models.Model):
    '''
    React Native 产品模型
    '''
    class Meta:

        verbose_name = 'React-Native-MiniModel'

        verbose_name_plural = "React-Native-MiniModel"

    # mini id
    miniId = models.CharField(max_length=30,
                              unique=True,
                              verbose_name='小程序ID',
                              help_text='建议使用 bundle ID，长度不能超过30')

    mobile_application_group = models.CharField(max_length=20, default='mini', verbose_name='group', help_text='不需要修改')
    # mobile_application_group = models.ForeignKey(MobileApplicationGroup,
    #                                              related_name='mini_mobile_application_group')

    def __str__(self):
        return self.miniId


# 小程序信息模型
class MiniInfoModel(models.Model):

    class Meta:

        verbose_name = 'React-Native-MiniInfo'

        verbose_name_plural = 'React-Native-MiniInfo'

    product = models.ForeignKey(MiniModel,
                                related_name='mini_info_product',
                                verbose_name='关联小程序',)

    name = models.CharField(max_length=15,
                            verbose_name='小程序名称',)

    icon = models.FileField(verbose_name='小程序头像',
                            help_text='以 jpg jpeg png 结尾 大小为 60 * 60',
                            upload_to=mini_icon_path,)

    distribution = models.BooleanField(default=False, verbose_name='发布上线')

# 小程序包模型
class MiniPackageModel(models.Model):
    '''
    React Native mini iOS 包模型
    '''
    class Meta:

        verbose_name = 'React-Native-MiniPackage'

        verbose_name_plural = 'React-Native-MiniPackage'

    product = models.ForeignKey(MiniModel,
                                related_name='mini_package_product',
                                verbose_name='关联产品',)

    platform = models.CharField(max_length=10,
                                default='ios',
                                verbose_name='平台',
                                help_text='ios or android')

    size = models.FloatField(verbose_name='文件大小')

    path = models.FileField(verbose_name='路径', help_text='上传zip文件', upload_to=mini_package_file_path)

    forceupdate = models.BooleanField(verbose_name='是否强制更新',
                                      help_text='设置为强制更新，将不会使用本地被缓存文件（当本地缓存或内置版本存在 bug 时一定置为 true）',
                                      default=False)

    createtime = models.DateTimeField(auto_now_add=True,
                                      verbose_name='上传时间')

    distribution = models.BooleanField(default=False, verbose_name='发布上线')

    history = models.BooleanField(default=False, verbose_name='历史版本')

    version = models.CharField(max_length=20, verbose_name='版本号', default='no version', help_text='标识版本号，但不会作为版本升级使用')

    versiondesc = models.CharField(max_length=50, verbose_name='发版说明', default='新版本')

    fullupdate = models.BooleanField(default=False, verbose_name='整包升级', help_text='是否是整包升级（设置为True时，不会读取补丁包）')

    def isIOS(self):
        return self.platform == 'ios'

    # def get_binary_url(self):
    #     if not self.path:
    #         return Nonew
    #     return remote_url(self.path.url, "https", self, self.product.miniId)

    def __str__(self):
        return '%s_%s' % (self.product, self.id)
