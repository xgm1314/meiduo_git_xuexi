# _*_coding : uft-8 _*_
# @Time : 2023/5/5 9:36
# @Author : 
# @File : utils
# @Project : meiduo_mall

import base64
import pickle

from django_redis import get_redis_connection
from django.http import JsonResponse


def merge_cart_cookie_redis(request, user, response):
    """ 登录后合并cookie购物车的数据到redis """

    cookie_cart_str = request.COOKIES.get('carts')  # 获取cookie中的数据
    if cookie_cart_str is None:
        return JsonResponse({'code': 400, 'errmsg': '购物车为空'})
    cookie_cart_dict = pickle.loads(base64.b64decode(cookie_cart_str))  # 对cookie中的信息进行解码
    new_cart_dict = {}  # 创建新的购物车
    new_cart_selected_add = []  # 创建添加选项的列表
    new_cart_selected_remove = []  # 创建移除选线的列表
    # 同步cookie中的数据
    for sku_id, cookie_dict in cookie_cart_dict.items():
        new_cart_dict[sku_id] = cookie_dict['count']
        print(cookie_dict['selected'])
        if cookie_dict['selected'] == True:
            new_cart_selected_add.append(sku_id)
        else:
            new_cart_selected_remove.append(sku_id)
    # 连接redis库，写入数据
    redis_cli = get_redis_connection('carts')
    redis_cli.hmset('carts_%s' % user.id, new_cart_dict)  # 将商品id和数量存在redis的哈希内
    if new_cart_selected_add:
        redis_cli.sadd('selected_%s' % user.id, *new_cart_selected_add)
    if new_cart_selected_remove:
        redis_cli.sadd('selected_%s' % user.id, *new_cart_selected_remove)
    response.delete_cookie('carts')
    return response
