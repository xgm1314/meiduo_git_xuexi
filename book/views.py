from django.shortcuts import render

# Create your views here.
from django.views.generic import View
from book.models import BookInfo
from django.http import JsonResponse
import json



"""
通过REST来实现 对于书籍的 增删改查操作

增加一本书籍
删除一本书籍
修改一本书籍
查询一本书籍
查询所有书籍
   
###########列表视图#################################    
查询所有书籍
GET             books/
    1.查询所有数据
    2.将查询结果集进行遍历,转换为字典列表
    3.返回响应
    
增加一本书籍
POST            books/
    1.接收参数,获取参数
    2.验证参数
    3.保存数据
    4.返回响应

###########详情视图#################################
删除一本书籍
DELETE          books/id/
    1. 接收参数,查询数据
    2. 操作数据库(删除)
    3. 返回响应
    
修改一本书籍
PUT             books/id/
    1.查询指定的数据
    2.接收参数,获取参数
    3.验证参数
    4.更新数据
    5.返回响应
查询一本书籍
GET             books/id/
    1.查询指定数据
    2.将对象数据转换为字典数据
    3.返回响应




######################################################################
###########列表视图#################################    
查询所有书籍
GET             books/
    1.查询所有数据                                    查询数据库
    2.将查询结果集进行遍历,转换为字典列表                 序列化操作
    3.返回响应                                        返回响应
    
增加一本书籍
POST            books/
    1.接收参数,获取参数                                 JSON/dict
    2.验证参数
    3.保存数据                                        反序列化操作
    4.返回响应                                        序列化操作

###########详情视图#################################
删除一本书籍
DELETE          books/id/
    1. 接收参数,查询数据                              查询
    2. 操作数据库(删除)                              删除
    3. 返回响应
    
修改一本书籍
PUT             books/id/   
    1.查询指定的数据                               对象
    2.接收参数,获取参数                         JSON/dict
    3.验证参数
    4.更新数据                                  反序列化
    5.返回响应                                  序列化
查询一本书籍
GET             books/id/
    1.查询指定数据
    2.将对象数据转换为字典数据                      序列化
    3.返回响应




"""


# Create your views here.
class BookListView(View):
    """
    查询所有图书、增加图书
    """
    def get(self, request):
        """
        查询所有图书
        路由：GET /books/
        """
        queryset = BookInfo.objects.all()
        book_list = []
        for book in queryset:
            book_list.append({
                'id': book.id,
                'name': book.name,
                'pub_date': book.pub_date
            })
        return JsonResponse(book_list, safe=False)

    def post(self, request):
        """
        新增图书
        路由：POST /books/
        """
        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book = BookInfo.objects.create(
            name=book_dict.get('name'),
            pub_date=book_dict.get('pub_date')
        )

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        },safe=False)

class BookDetailView(View):
    """
    获取单个图书信息
    修改图书信息
    删除图书
    """
    def get(self, request, pk):
        """
        获取单个图书信息
        路由： GET  /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        json_bytes = request.body
        json_str = json_bytes.decode()
        book_dict = json.loads(json_str)

        # 此处详细的校验参数省略

        book.name = book_dict.get('name')
        book.pub_date = book_dict.get('pub_date')
        book.save()

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({},status=404)

        book.delete()

        return JsonResponse({},status=204)

"""
我们的序列化器 目的
1. 将对象转换为字典数据

"""
from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 1. 模拟查询一个对象
book=BookInfo.objects.get(id=1)

# BookInfoSerializer(instance=对象,data=字典)
# 2.实例化序列化,将对象数据传递给序列化器
serializer=BookInfoSerializer(instance=book)

# 3.获取序列化器将对象转换为字典的数据
serializer.data


##########################################

from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 1. 获取所有书籍
books=BookInfo.objects.all()
# 2. 实例化序列化,将对象数据传递给序列化器
serializer=BookInfoSerializer(instance=books,many=True)
# serializer=BookInfoSerializer(books)   正确的写法
# 3. 获取序列化(将对象转换为字典)的数据
serializer.data

"""
[
OrderedDict([('id', 1), ('name', '射雕英雄传'), ('pub_date', '1980-05-01'), ('readcount', 12)]), 
OrderedDict([('id', 2), ('name', '天龙八'),('pub_date', '1986-07-24'), ('readcount', 36)]), 
OrderedDict([('id', 3), ('name', '笑傲江湖'), ('pub_date', '1995-12-24'), ('readcount', 20)]), 
OrderedDict([('id', 4), ('name', '雪山飞狐'), ('pub_date', '1987-11-11'), ('readcount', 58)])
]

"""