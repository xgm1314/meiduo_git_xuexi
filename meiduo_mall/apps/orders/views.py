import json

from django.shortcuts import render

# Create your views here.
from django.views import View
from django_redis import get_redis_connection
from django.http import JsonResponse

from utils.views import LoginRequiredJSONMixin

from apps.users.models import Address
from apps.goods.models import SKU
from apps.orders.models import OrderInfo, OrderGoods


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
        order_id = timezone.now().strftime('%Y%m%d%H%M%S%f') + '%09d' % user.id  # 生成订单编号
        # order_id = datetime.now().strftime('%Y%m%d%H%M%S') + '%09d' % user.id  # 生成订单编号
        if pay_method == OrderInfo.PAY_METHODS_ENUM['CASH']:
            status = OrderInfo.ORDER_STATUS_ENUM['UNSEND']
        else:
            status = OrderInfo.ORDER_STATUS_ENUM['UNPAID']
        total_count = 0  # 商品总数量
        from decimal import Decimal
        total_amount = Decimal('0')  # 商品总金额
        freight = Decimal('10.00')  # 运费

        from django.db import transaction
        with transaction.atomic():
            point = transaction.savepoint()  # 事务开始点

            orderinfo = OrderInfo.objects.create(
                order_id=order_id,
                user=user,
                address=address_id,
                total_count=total_count,
                total_amount=total_amount,
                freight=freight,
                pay_method=pay_method,
                status=status
            )

            redis_cli = get_redis_connection('carts')  # 连接redis库
            pipeline = redis_cli.pipeline()  # 创建pipeline管道
            pipeline.hgetall('carts_%s' % user.id)
            pipeline.smembers('selected_%s' % user.id)
            result = pipeline.execute()  # 接受管道，返回结果
            # print(result)
            sku_id_counts = result[0]  # 获取哈希结果
            # print(sku_id_counts)
            selected_ids = result[1]  # 获取集合结果

            carts = {}  # 重新组织商品的勾选字典
            for sku_id in selected_ids:
                carts[int(sku_id)] = int(sku_id_counts[sku_id])

            for sku_id, count in carts.items():
                sku = SKU.objects.get(id=sku_id)  # 查询商品
                if sku.stock < count:
                    transaction.savepoint_rollback(point)  # 事务回滚点

                    return JsonResponse({'code': 400, 'errmsg': '商品数量不足'})

                from time import sleep
                sleep(5)

                old_stock = sku.stock  # 查询数据库的库存数据

                # sku.stock = sku.stock - count  # 库存减少
                # sku.sales = sku.sales + count  # 售量增加
                # sku.save()  # 保存

                new_stock = sku.stock - count  # 更新的库存数量
                new_sales = sku.sales + count  # 更新的售量

                # 如果查询的库存数量等于最初的数量，则更新，否则不更新
                result = SKU.objects.filter(id=sku_id, stock=old_stock).update(stock=new_stock, sales=new_sales)
                # print(result)
                if result == 0:  # 1:表示为真，0:为假
                    transaction.savepoint_rollback(point)  # 事务回滚点
                    return JsonResponse({'code': 400, 'errmsg': '下单失败~~~~~~~~~~~~~~~~~~~~'})

                orderinfo.total_count = orderinfo.total_count + count  # 商品总数量
                orderinfo.total_amount = orderinfo.total_amount + (sku.price * count) + freight  # 商品总价格
                OrderGoods.objects.create(
                    order_id=order_id,
                    sku=sku,
                    count=count,
                    price=sku.price
                )
            orderinfo.save()

            transaction.savepoint_commit(point)  # 事务提交点

        return JsonResponse({'code': 0, 'errmsg': 'ok', 'order_id': order_id})


"""
解决并发的超卖问题：
① 队列
② 锁
    悲观锁： 当查询某条记录时，即让数据库为该记录加锁，锁住记录后别人无法操作

            悲观锁类似于我们在多线程资源竞争时添加的互斥锁，容易出现死锁现象

    举例：

    甲   1,3,5,7

    乙   2,4,7,5


    乐观锁:    乐观锁并不是真的锁。
            在更新的时候判断此时的库存是否是之前查询出的库存，
            如果相同，表示没人修改，可以更新库存，否则表示别人抢过资源，不再执行库存更新。



    举例：
                桌子上有10个肉包子。  9    8 

                现在有5个人。 这5个人，每跑1km。只有第一名才有资格吃一个肉包子。 

                5

                4

                3 

    步骤：
            1. 先记录某一个数据  
            2. 我更新的时候，再比对一下这个记录对不对  


MySQL数据库事务隔离级别主要有四种：

    Serializable：串行化，一个事务一个事务的执行。  用的并不多

    Repeatable read：可重复读，无论其他事务是否修改并提交了数据，在这个事务中看到的数据值始终不受其他事务影响。

v    Read committed：读取已提交，其他事务提交了对数据的修改后，本事务就能读取到修改后的数据值。

    Read uncommitted：读取未提交，其他事务只要修改了数据，即使未提交，本事务也能看到修改后的数据值。


    举例：     5,7 库存 都是  8

    甲   5,   7        5

    乙  7,    5         5


MySQL数据库默认使用可重复读（ Repeatable read）


"""