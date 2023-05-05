from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse

from utils.views import LoginRequiredJSONMixin

from apps.users.models import Address
from apps.goods.models import SKU


class OrderSettlementView(LoginRequiredJSONMixin, View):
    """ 订单页面 """

    def get(self, request):
        user = request.user  # 获取用户信息
        addresses = Address.objects.filter(is_deleted=False)  # 查询用户的地址信息
        addresses_list = []  # 将对象数据转化为字典数据
        for address in addresses:
            addresses_list.append({
                'id': address.id,
                'province': address.province.name,
                'city': address.city.name,
                'district': address.district.name,
                'place': address.place,
                'receiver': address.receiver,
                'mobile': address.mobile
            })
        redis_cli = get_redis_connection('carts')  # 连接redis库
        pipeline = redis_cli.pipeline()  # 创建pipeline管道
        pipeline.hgetall('carts_%s' % user.id)
        pipeline.smembers('selected_%s' % user.id)
        result = pipeline.execute()  # 接受管道，返回结果
        # print(result)
        sku_id_counts = result[0]  # 获取哈希结果
        # print(sku_id_counts)
        selected_ids = result[1]  # 获取集合结果
        # print(selected_ids)
        selected_carts = {}
        for sku_id in sku_id_counts:  # 将哈希结果转换为字典
            selected_carts[int(sku_id)] = int(sku_id_counts[sku_id])
        # print(selected_carts)
        sku_list = []
        for sku_id, count in selected_carts.items():
            sku = SKU.objects.get(id=sku_id)
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'count': count,
                'default_image': sku.default_image.url,
                'price': sku.price
            })
        # print(sku_list)

        from decimal import Decimal
        freight = Decimal(10)  # Decimal货币类型

        context = {
            'skus': sku_list,
            'addresses': addresses_list,
            'freight': freight  # 运费
        }
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'context': context})
