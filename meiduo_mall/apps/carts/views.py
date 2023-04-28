import json

from django.shortcuts import render

# Create your views here.
"""
import pickle
import base64

data = {
    'user1': {'count': 10, 'selected': True},
    'user2': {'count': 20, 'selected': False}
}
data_bytes = pickle.dumps(data)  # 将字典数据转化为二进制数据
data_encode = base64.b64encode(data_bytes)  # 将二进制数据进行编码

data_decode = base64.b64decode(data_encode)  # 将二进制数据进行编码
data_loads = pickle.loads(data_decode)  # 将二进制数据转化为字典数据
"""
from django.http import JsonResponse

from django.views import View
from django_redis import get_redis_connection

from apps.goods.models import SKU


class CartView(View):
    """ 购物车 """

    def post(self, request):
        """ 新增购物车 """
        body_dict = json.loads(request.body.decode())  # 获取前端传入的数据
        sku_id = body_dict.get('sku_id')
        count = body_dict.get('count')
        selected = body_dict.get('selected')
        user = request.user
        print(user)
        # 验证数据
        try:
            sku = SKU.objects.get(id=sku_id)  # 查询数据库是否有该商品
        except SKU.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '该商品不存在'})
        try:
            count = int(count)  # 格式化传入的数量
        except Exception:
            count = 1
        if selected is None:  # 如果传入的是空，则默认勾选
            selected = True
        if user.is_authenticated:  # 判断用户是否登录
            redis_cli = get_redis_connection('carts')  # 连接数据库
            redis_cli.hset('carts_%s' % user.id, sku_id, count)  # 将商品id和数量存在redis的哈希内
            if selected == True:
                redis_cli.sadd('selected_%s' % user.id, sku_id)  # 将是否被勾选的id存在redis的集合中
            return JsonResponse({'code': 0, 'errmsg': 'ok'})
        else:
            carts = {  # 未登录用户，创建字典
                sku_id: {'count': count, 'selected': selected}
            }
            import pickle
            data_bytes = pickle.dumps(carts)  # 将字典转换为二进制数据
            import base64
            data_encode = base64.b64encode(data_bytes)  # 将二进制数据进行编码
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('carts', data_encode.decode(), 3600 * 24 * 7)
            return response
