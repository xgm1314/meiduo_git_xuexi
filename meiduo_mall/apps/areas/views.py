from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse

from apps.areas.models import Area


class AreaView(View):
    """ 省份查询 """

    def get(self, request):
        provinces = Area.objects.filter(parent=None)  # 获取省份对象
        province_list = []  # 定义空列表
        for province in provinces:
            province_list.append({
                'id': province.id,
                'name': province.name
            })
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'province_list': province_list})
