# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from .model_measureUnit import ProductMeasureUnit

from .models import *

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)

class ProductCategoryAdmin(admin.ModelAdmin):

    list_display = ['id', 'code', 'name']

    search_fields = ['name']
admin.site.register(ProductCategory, ProductCategoryAdmin)

class MeasureUnitAdmin(admin.ModelAdmin):

    list_display = ['id', 'code', 'name']

    search_fields = ['name']

admin.site.register(ProductMeasureUnit, MeasureUnitAdmin)