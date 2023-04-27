# _*_coding : uft-8 _*_
# @Time : 2023/4/26 19:49
# @Author : 
# @File : crons
# @Project : meiduo_mall
import time
import datetime

from apps.contents.models import ContentCategory

from utils.goods import get_categories


def generic_meiduo_index():
    # print('-----------%s-------------' % time.ctime())
    times = datetime.datetime.now()  # 获取当前时间
    print(times)
    categories = get_categories()  # 商品数据
    contents = {}
    content_categories = ContentCategory.objects.all()
    for cat in content_categories:
        contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
    content = {
        'categories': categories,
        'contents': contents
    }
    # 加载渲染的模板
    from django.template import loader
    index_template = loader.get_template('index.html')
    # 把数据给模板
    index_html_data = index_template.render(content)
    # 把渲染好的HTML写入到指定的文件
    from meiduo_mall import settings
    import os
    file_path = os.path.join(os.path.dirname(settings.BASE_DIR), 'templates/index.html')  # base_dir的上一级目录
    # file_path = os.path.join('templates/index.html')  # base_dir的templates目录
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(index_html_data)
