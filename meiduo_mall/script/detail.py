# _*_coding : uft-8 _*_
# @Time : 2023/4/27 12:44
# @Author : 
# @File : detail
# @Project : meiduo_mall
# 详情页面生成

# ../ 当前目录的上一级目录
import sys

sys.path.insert(0, '../')

# 告诉 os django的配置文件
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')

# django.setup() 相当于当前文件有django的配置环境
import django

django.setup()

from django.http import JsonResponse

from apps.goods.models import SKU

from utils.goods import get_goods_specs, get_categories, get_breadcrumb


def generic_detail_html(sku):
    try:
        sku = SKU.objects.get(id=sku.id)
    except SKU.DoesNotExist:
        return JsonResponse({'code': 0, 'errmsg': '该数据不存在'})
    # 分类数据
    categories = get_categories()
    # 面包屑数据
    breadcrumb = get_breadcrumb(sku.category)
    # 规格信息
    goods_specs = get_goods_specs(sku)
    content = {
        'categories': categories,
        'breadcrumb': breadcrumb,
        'sku': sku,
        'specs': goods_specs,
    }

    from django.template import loader
    index_template = loader.get_template('detail.html')  # 加载渲染的模板
    index_html_data = index_template.render(content)  # 把数据给模板
    from meiduo_mall import settings
    import os
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'templates/goods/%s.html' % sku.id)  # 把渲染好的HTML写道指定文件中
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(index_html_data)


if __name__ == '__main__':
    skus = SKU.objects.all()
    for sku in skus:
        generic_detail_html(sku)
