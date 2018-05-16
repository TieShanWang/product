# -*- coding: utf-8 -*-

from django.http import HttpResponse
from rest_framework import authentication
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.views import APIView

from .models import MiniPackageModel, MiniInfoModel, MiniModel
from django.contrib.sites.models import Site

import logging

logger = logging.getLogger("django")


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

def res_with_success(data):
    return JSONResponse(status=200, data={
        'code': '200',
        'data': data,
        'message': 'success'
 })

def res_with_empty_data(message):
    return JSONResponse(status=200, data={
        'code': '500',
        'data': {
        },
        'message': message
 })

def res_with_not_mini():
    return JSONResponse(status=200, data={
        'code': '501',
        'data': {
        },
        'message': 'not found mini'
 })

def res_with_not_mini_config():
    return JSONResponse(status=200, data={
        'code': '502',
        'data': {
        },
        'message': 'not found mini config'
 })

def res_with_not_mini_package():
    return JSONResponse(status=200, data={
        'code': '503',
        'data': {
        },
        'message': 'not found mini package'
 })

class MiniApiView(APIView):

    parser_classes = (MultiPartParser, FormParser,)
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):

        logger.info('mini has get file upload. info vvv')
        logger.info(request.data)

        data = request.data

        if not 'file' in data:
            return res_with_empty_data('no file found')
        if not data.get('version'):
            return res_with_empty_data('empty version')
        if not data.get('product'):
            return res_with_empty_data('empty product')
        if not data.get('platform'):
            return res_with_empty_data('empty platform')
        if data['platform'].lower() not in ['ios', 'android']:
            return res_with_empty_data('platform must be ios or android')

        # 绑定的小程序ID
        miniId = request.data['product']

        # find mini model
        try:
            miniModels = MiniModel.objects.filter(miniId=miniId)
            if not len(miniModels):
                raise MiniModel.DoesNotExist
        except MiniModel.DoesNotExist:
            return res_with_not_mini()

        platform = data['platform'].lower()
        file_obj = request.data['file']
        version = request.data.get('version')
        distribution = request.data['distribution'] == '1'
        versiondesc = request.data.get('versiondesc') or '新版本'
        forceupdate = request.data.get('forceupdate') == '1'
        size = request.data.get('size') or 0

        try:
            size = float(size)
        except:
            size = 0

        if distribution:
            try:
                agreements = MiniPackageModel.objects.filter(product__miniId=miniId, distribution=distribution, platform=platform)
                for info in agreements:
                    if info.distribution:
                        info.distribution = False
                        info.history = True
                    info.save()

            except MiniPackageModel.DoesNotExist:
                print("MiniPackageModel is empty.")

        info_model = MiniPackageModel(distribution=distribution,
                                      versiondesc=versiondesc,
                                      path=file_obj,
                                      size=size,
                                      history=False,
                                      forceupdate=forceupdate,
                                      version=version,
                                      product=miniId,
                                      platform=platform)

        info_model.save()

        return res_with_success({})

# 小程序信息
@api_view(['POST'])
def mini_info(request):

    logger.info('get request for mini info')

    data = request.data

    logger.info('data is : %s' % data)

    if not data:
        return res_with_empty_data('empty data')
    if not data.get('miniId'):
        return res_with_empty_data('empty miniId')

    miniId = data.get('miniId')

    # find mini model
    # try:
    #     miniModels = MiniModel.objects.filter(miniId=miniId)
    #     if not len(miniModels):
    #         raise MiniModel.DoesNotExist
    # except MiniModel.DoesNotExist:
    #     return res_with_not_mini()

    # find mini version info
    try:
        miniInfoModels = MiniInfoModel.objects.filter(product__miniId=miniId, distribution=True)
        if not len(miniInfoModels):
            raise MiniInfoModel.DoesNotExist
    except MiniInfoModel.DoesNotExist:
        return res_with_not_mini_config()

    # info model
    infoModel = miniInfoModels.first()

    return res_with_success({
        'miniId': miniId,
        'name': infoModel.name,
        'iconURL': parse_to_url_http(infoModel.icon.url),
        'version': infoModel.id
    })


# 处理获取包的版本信息
# f_version 当前版本
# product   所属产品
# platform  平台
@api_view(['POST'])
def mini_version(request):

    logger.info("get request for mini update info")

    logger.info('data: %s' % request.data)

    logger.info(request.data)

    data = request.data

    if not data:
        return res_with_empty_data('empty data')
    if not data.get('miniId'):
        return res_with_empty_data('empty miniId')
    if not data.get('platform'):
        return res_with_empty_data('empty platform')

    platform = data.get('platform').lower()

    if platform not in ['ios', 'android']:
        return res_with_empty_data('platform must be one of [ios, android]')

    miniId = data.get('miniId')

    # local version
    f_version = data.get('f_version')

    # find mini model
    # try:
    #     miniModels = MiniModel.objects.filter(miniId=miniId)
    #     if not len(miniModels):
    #         raise MiniModel.DoesNotExist
    # except MiniModel.DoesNotExist:
    #     return res_with_not_mini()

    # find mini package
    try:
        miniPackageModels = MiniPackageModel.objects.filter(product__miniId=miniId, distribution=True, platform=platform)
        if not len(miniPackageModels):
            raise MiniPackageModel.DoesNotExist
    except MiniPackageModel.DoesNotExist:
        return res_with_not_mini_package()

    packageModel = miniPackageModels.first()

    return res_with_success({
                'miniId': miniId,
                'version': packageModel.id,
                'forceupdate': packageModel.forceupdate,
                'description': packageModel.versiondesc,
                'path': parse_to_url_http(packageModel.path.url),
                # 'path': packageModel.get_binary_url(),
                'fullupdate': packageModel.fullupdate,
            })


def parse_to_url_https(subPath):

    return parse_to_url(subPath, "https")


def parse_to_url_http(subPath):

    return parse_to_url(subPath, "http")


def parse_to_url(subPath, pre):

    # Site.objects.clear_cache()

    current_site = Site.objects.get_current()

    sub = '%s/%s' % (current_site.domain, subPath)

    sub = sub.replace('//', '/')

    return '%s://%s' % (pre, sub)
