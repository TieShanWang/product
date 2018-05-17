# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import MiniInfoModel, MiniPackageModel, MiniModel

# Register your models here.

class MiniModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'miniId', 'mobile_application_group']

    list_search = ['miniId']

    fields = ['miniId', 'mobile_application_group']


admin.site.register(MiniModel, MiniModelAdmin)


class MiniInfoModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'distribution', 'name', 'product', 'icon']

    list_filter = ['product', 'distribution', 'name']

    fields = ['name', 'product', 'icon', 'distribution']

    def save_model(self, request, obj, form, change):

        if obj.distribution:
            try:
                agreements = MiniInfoModel.objects.filter(distribution=True,
                                                          product__miniId=obj.product.miniId).exclude(pk=obj.id)
                for info in agreements:
                    info.distribution = False
                    info.save()

            except MiniInfoModel.DoesNotExist:
                print("MiniInfoModel is empty.")

        obj.save()


admin.site.register(MiniInfoModel, MiniInfoModelAdmin)


class MiniPackageModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'version', 'distribution', 'forceupdate', 'fullupdate', 'platform', 'createtime', 'product',
                    'show_file_size', 'history', 'path']

    list_search = ['id', 'version', 'platform']

    fields = ['product', 'platform', 'path', 'version', 'versiondesc', 'size', 'fullupdate', 'forceupdate',
              'distribution']

    list_filter = ['product', 'platform']

    def show_file_size(self, obj):
        return '%.2fM' % obj.size

    show_file_size.short_description = '文件大小'

    def save_model(self, request, obj, form, change):

        if obj.distribution:
            try:
                agreements = MiniPackageModel.objects.filter(distribution=True,
                                                             product__miniId=obj.product.miniId).exclude(pk=obj.id)
                for info in agreements:
                    info.distribution = False
                    info.history = True
                    info.save()

            except MiniPackageModel.DoesNotExist:
                print("RNPackageModel is empty.")

        obj.save()


admin.site.register(MiniPackageModel, MiniPackageModelAdmin)