# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework.response import Response

from rest_framework.views import APIView

from .models import *

# import the logging library
import logging

# Get an instance of a logger
logger = logging.getLogger("React native")

class JSONResponse(Response):
    def __init__(self, code='200', message='success', data=None):

        responsedata = {
            'code': code,
            'message': message,
            'data': data,
        }

        super(JSONResponse, self).__init__(responsedata, status=200, content_type='application/json')


class ProductView(APIView):

    def post(self, request, format=None):

        all_objects = Product.objects.all()

        return JSONResponse(data=[p.toJson() for p in all_objects])


class ProductCategoryView(APIView):

    def post(self, request, format=None):

        all_objects = ProductCategory.objects.all()

        return JSONResponse(data=[p.toJson() for p in all_objects])


class ProductMeasureUnitView(APIView):

    def post(self, request, format=None):

        all_objects = ProductMeasureUnit.objects.all()

        return JSONResponse(data=[p.toJson() for p in all_objects])

class ProductAddMeasureUnitView(APIView):

    def post(self, request, format=None):

        data = request.data

        code = data['code']

        name = data['name']

        if not code or not name:
            return JSONResponse(code='500', message='请输入正确的编码和名称')

        new = ProductMeasureUnit()

        new.name = name

        new.code = code

        new.save()

        return JSONResponse()

class ProductAddCategoryView(APIView):

    def post(self, request, format=None):

        data = request.data

        code = data['code']

        name = data['name']

        if not code or not name:
            return JSONResponse(code='500', message='请输入正确的编码和名称')

        new = ProductCategory()

        new.name = name

        new.code = code

        new.save()

        return JSONResponse()