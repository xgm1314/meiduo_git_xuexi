import datetime

from django.shortcuts import render
from django.views import View
from collections import Counter, OrderedDict
from django.http import JsonResponse

# Create your views here.
from apps.goods.models import GoodsChannel, GoodsCategory, SKU
from apps.contents.models import ContentCategory
from utils.goods import get_categories
from utils.goods import get_breadcrumb


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


class ListView(View):
    """ 排行 """

    def get(self, request, nid):
        # ordering = 'price'  # 排序字段
        ordering = request.GET.get('ordering')  # 排序字段
        # page_size = 5  # 每页多少数据
        page_size = request.GET.get('page_size')  # 每页多少数据
        # page = 1  # 第几页数据
        page = request.GET.get('page')  # 第几页数据
        try:
            category = GoodsCategory.objects.get(id=nid)
        except GoodsCategory.DoesNotExist:
            return JsonResponse({'code': 0, 'errmsg': '参数不全'})
        breadcrumb = get_breadcrumb(category)  # 面包屑数据
        skus = SKU.objects.filter(category=category, is_launched=True).order_by(ordering)
        from django.core.paginator import Paginator
        paginator = Paginator(skus, per_page=page_size)  # skus列表数据，per_page每页的数据
        page_skus = paginator.page(page)  # 获取指定页码的数据
        sku_list = []
        for sku in page_skus.object_list:
            sku_list.append({
                'id': sku.id,
                'name': sku.name,
                'price': sku.price,
                'default_image': sku.default_image.url
            })
        total = paginator.num_pages
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'list': sku_list, 'count': total, 'breadcrumb': breadcrumb})


from haystack.views import SearchView


class SKUSearchView(SearchView):
    """ 搜索框 """

    def create_response(self):
        """ 获取搜索结果 """
        context = self.get_context()  # 通过断点来判断返回的数据类型
        sku_list = []
        for sku in context['page'].object_list:
            sku_list.append({
                'id': sku.object.id,
                'name': sku.object.name,
                'price': sku.object.price,
                'default_image_url': sku.object.default_image.url,
                'searchkey': context.get('query'),
                'page_size': context['page'].paginator.num_pages,
                'count': context['page'].paginator.count
            })
        return JsonResponse(sku_list, safe=False)


from utils.goods import get_goods_specs


class DetailView(View):
    def get(self, request, sku_id):
        try:
            sku = SKU.objects.get(id=sku_id)
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
        return render(request, 'detail.html', content)
