import json

from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse

from utils.views import LoginRequiredJSONMixin

from apps.users.models import Address
from apps.goods.models import SKU
from apps.orders.models import OrderInfo


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


class OrderCommitView(LoginRequiredJSONMixin, View):
    """ 提交订单 """
    """
    {
        "address":2,
        "pay_method":1
    }
    """

    def post(self, request):
        user = request.user  # 获取前端传入的数据
        body_dict = json.loads(request.body.decode())
        address = body_dict.get('address')
        pay_method = body_dict.get('pay_method')

        # 验证传入的数据
        if not all([address, pay_method]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        try:
            address_id = Address.objects.get(id=address)  # 查找表中是否有这个地址的对象
        except Address.DoesNotExist:
            return JsonResponse({'code': 400, 'errmsg': '用户地址不存在'})
        if pay_method not in (
                OrderInfo.PAY_METHODS_ENUM['CASH'],
                OrderInfo.PAY_METHODS_ENUM['ALIPAY']):  # 等同于if pay_method not in(1,2)
            return JsonResponse({'code': 400, 'errmsg': '支付方式不正确'})
        from django.utils import timezone
        from datetime import datetime
        # timezone.now()  时间格式(获取当前时间)
        # datetime.strftime()=timezone.localtime().strftime('%Y%m%d%H%M%S')
        order_id = timezone.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id  # 生成订单编号
        # order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id  # 生成订单编号
        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        else:
            status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']
        total_count = 0  # 商品总数量
        from decimal import Decimal
        total_amount = Decimal('0')  # 商品总金额
        freight = Decimal('10.00')  # 运费

        OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            # address=address,
            address=address_id,  # 测试用
            total_count=total_count,
            total_amount=total_amount,
            freight=freight,
            pay_method=pay_method,
            status=status
        )

        return JsonResponse({'code': 0, 'errmsg': 'ok'})
