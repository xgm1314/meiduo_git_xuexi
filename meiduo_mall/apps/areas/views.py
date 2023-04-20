from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.core.cache import cache

from apps.areas.models import Area


class AreaView(View):
    """ 省份查询 """

    def get(self, request):

        province_list = cache.get('province')  # 读取缓存
        if province_list is None:  # 判断缓存是否存在

            provinces = Area.objects.filter(parent=None)  # 获取省份对象
            province_list = []  # 定义空列表
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })

            cache.set('province', province_list, 3600)  # 设置缓存

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})


class SubAreaView(View):
    """ 查询市、区县 """

    def get(self, request, id):

        data_list = cache.get('city_%s' % id)  # 读取缓存
        if data_list is None:

            # # 方式一:
            # up_level=Area.objects.filter(id=id)  # 获取市
            # down_level = Area.objects.filter(parent_id=id)  # 获取区县对象

            # 方式二:
            up_level = Area.objects.get(id=id)  # 获取市
            down_level = up_level.subs.all()  # 获取区县对象

            data_list = []
            # # 方式一:
            # for i in up_level:
            #     data_list.append({'id': i.id, 'name': i.name})

            # # 方式二:
            data_list.append({'id': id, 'name': up_level.name})

            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                })

            cache.set('city_%s' % id, data_list, 3600)  # 设置缓存

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list}})
