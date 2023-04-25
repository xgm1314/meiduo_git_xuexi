from django.shortcuts import render
from django.views import View
from collections import Counter, OrderedDict
from django.http import JsonResponse

# Create your views here.
from apps.goods.models import GoodsChannel
from apps.contents.models import ContentCategory
from utils.goods import get_categories


class IndexView(View):
    """ 页面展示 """

    """
    def get(self, request):
        categories = OrderedDict()  # 初始化一个有序字典
        channels = GoodsChannel.objects.order_by('group_id', 'sequence')  # 根据排序查询数据
        for channel in channels:
            group_id = channel.group_id  # 获取当前组
            if group_id is not categories:
                categories[group_id] = {'channels': [], 'sub_cats': []}  # 初始化二级标题
            cat1 = channel.category  # 当前频道的类别
            categories[group_id]['channels'].append({
                'id': cat1.id,
                'name': cat1.name,
                'url': channel.url
            })
            for cat2 in cat1.subs.all():
                cat2.sub_cats = []
                for cta3 in cat2.subs.all():
                    cat2.sub_cats.append(cta3)
                categories[group_id]['sub_cats'].append(cat2)
        return categories
        """

    def get(self, request):
        categories = get_categories()  # 商品数据
        contents = {}
        content_categories = ContentCategory.objects.all()
        for cat in content_categories:
            contents[cat.key] = cat.content_set.filter(status=True).order_by('sequence')
        content = {
            'categories': categories,
            'contents': contents
        }
        return render(request, 'index.html', content)
