# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from django.db import models

from .MeasureUnit import MeasureUnit

from .models import *

import shutil

import os

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    pass
admin.site.register(Product, ProductAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'type', 'name']
admin.site.register(ProductCategory, ProductCategoryAdmin)


class MeasureUnitAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name']

admin.site.register(MeasureUnit, MeasureUnitAdmin)