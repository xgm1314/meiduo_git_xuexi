###################序列化###############################
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

    """
    def get(self,request):
        books=BookInfo.objects.all()
        book_list=[]
        for book in books:
            book_list.append({
                'id':book.id,
                'name':book.name,
                'pub_date':book.pub_date
            })
        return JsonResponse(book_list,safe=False)
    """

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
        }, safe=False)


"""
    def post(self, request):
        body_dict = json.loads(request.body.decode())
        name = body_dict.get('name')
        pub_date = body_dict.get('pub_date')
        if not all([name, pub_date]):
            return JsonResponse({},status=404)
        book = BookInfo.objects.create(
            name=name,
            pub_date=pub_date
        )
        book.save()
        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        }, safe=False)
"""


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
            return JsonResponse({}, status=404)

        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })

    """    
    def get(self, request, pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)
        else:
            return JsonResponse({
                'id': book.id,
                'name': book.name,
                'pub_date': book.pub_date
            })
    """

    def put(self, request, pk):
        """
        修改图书信息
        路由： PUT  /books/<pk>
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

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

    """
    def put(self, request, pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

        body_dict = json.loads(request.body.decode())
        name = body_dict.get('name')
        pub_date = body_dict.get('pud_date')
        if not all([name, pub_date]):
            return JsonResponse({}, status=404)
        book.name = name
        book.pub_date = pub_date
        book.save()
        return JsonResponse({
            'id': book.id,
            'name': book.name,
            'pub_date': book.pub_date
        })
    """

    def delete(self, request, pk):
        """
        删除图书
        路由： DELETE /books/<pk>/
        """
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)

        book.delete()

        return JsonResponse({}, status=204)

    """
    def delete(self, request, pk):
        try:
            book = BookInfo.objects.get(id=pk)
        except BookInfo.DoesNotExist:
            return JsonResponse({}, status=404)
        book.delete()
        return JsonResponse({}, status=204)
    """


"""
我们的序列化器 目的
1. 将对象转换为字典数据

"""
from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 1. 模拟查询一个对象
book = BookInfo.objects.get(id=1)

# BookInfoSerializer(instance=对象,data=字典)
# 2.实例化序列化,将对象数据传递给序列化器
serializer = BookInfoSerializer(instance=book)

# 3.获取序列化器将对象转换为字典的数据
serializer.data

##########################################

from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 1. 获取所有书籍
books = BookInfo.objects.all()
# 2. 实例化序列化,将对象数据传递给序列化器
serializer = BookInfoSerializer(instance=books, many=True)  # 如果是多个值(查询结果集)many=True
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

#########################外键的序列化器的定义 验证###########################################################################

from book.serializers import PeopleInfoSerializer
from book.models import PeopleInfo

# 1.  模拟查询对象
person = PeopleInfo.objects.get(id=1)

# 2. 创建序列化器
serializer = PeopleInfoSerializer(instance=person)

# 3. 获取序列化器中 将对象转换为字典的数据
serializer.data

######################反序列化##########################################

"""
序列化器验证数据的第一种形式:

1.  我们定义的数据类型,可以帮助我们 在反序列化(字典转模型)的时候 验证传入的数据的类型
    例如:
        DateField 需要满足 YYYY-MM-DD
        IntegerField 满足整形类型

2.  通过字段的选项来验证数据
    例如: 
        CharField(max_length=10,min_length=5)
        IntegerField(max_value=10,min_value=1)
        required=True 默认是True

        read_only: 只用于序列化使用. 反序列化的时候 忽略该字段
        write_only: 只是用于反序列化使用. 序列化的时候 忽略该字段
"""

from book.serializers import BookInfoSerializer

# 模拟接受字典数据
data = {
    # 'id': 5,
    'name': 'python',
    'pub_date': '2021-06-09',
    'readcount': 666,
    'commentcount': 10
}
# 创建序列化器
# instance 用于序列化 对象转字典
# data 用于反序列化 字典转对象
serializer = BookInfoSerializer(data=data)
# 验证数据 数据正确返回True，不正确返回False
serializer.is_valid(raise_exception=True)
# 保存到数据库
serializer.save()

##
from book.serializers import BookInfoSerializer
from book.models import BookInfo

# 模拟对象数据
book = BookInfo.objects.get(id=18)
# 模拟接受字典数据
data = {
    # 'id': 5,
    'name': 'python基础11',
    'pub_date': '2022-06-09',
    'readcount': 666,
    'commentcount': 1
}
# 创建序列化器
# instance 用于序列化 对象转字典
# data 用于反序列化 字典转对象
serializer = BookInfoSerializer(instance=book, data=data)
# 验证数据 数据正确返回True，不正确返回False
serializer.is_valid(raise_exception=True)
# 保存到数据库
serializer.save()
serializer.data

from book.serializers import BoolInfoModelSerializer

# BoolInfoModelSerializer()
data = {
    # 'id': 5,
    'name': 'python进阶',
    'pub_date': '2022-06-09',
    'readcount': 666,
    'commentcount': 1
}
serializer = BoolInfoModelSerializer(data=data)
serializer.is_valid(raise_exception=True)
serializer.save()

#########################################################################
# 传入book(外键)
from book.serializers import BoolInfoModelSerializer, PeopleInfoModelSerializer
from book.models import BookInfo, PeopleInfo

# 1、模拟字典数据
data = {
    'book': 1,
    'name': 'hzmlfyq',
    'password': '123456'
}
serializer = PeopleInfoModelSerializer(data=data)
serializer.is_valid(raise_exception=True)
serializer.save()
# 传入book_id(外键),需要重写字段book_id
from book.serializers import BoolInfoModelSerializer, PeopleInfoModelSerializer1
from book.models import BookInfo, PeopleInfo

# 1、模拟字典数据
data = [
    {
        'book_id': 1,
        'name': 'hzmlfyq04',
        'password': '123456',
        'is_delete': True,  # 传递不需要的数据，需要用read_only过滤掉
        'description': 'qq'
    },
    {
        'book_id': 2,
        'name': 'hzmlfyq05',
        'password': '123456',
        'is_delete': True,  # 传递不需要的数据，需要用read_only过滤掉
        'description': 'qq'
    },
]
serializer = PeopleInfoModelSerializer1(data=data, many=True)
serializer.is_valid(raise_exception=True)
serializer.save()

# # 这个data 就类似于 我们在讲解 序列化的时候
# 定义了一个 PeopleInfoSerializer
# 定义了一个 BookInfoSerialzier
# 在BookInfoSerialzier 有一个字段是 peopleinfo=PeopleInfoSerializer(many=True)
"""
class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(label='ID')

class BookInfoSerializer(serializers.Serializer):
    name = serializers.CharField(label='名称')

    #一本书籍关联多个人物
    people=PeopleInfoSerializer(many=True)

"""
from book.serializers import BoolInfoModelSerializer1

data = {
    'name': 'django',
    'people': [
        {
            'name': 'hzmlfyq04',
            'password': '123456',
        },
        {
            'name': 'hzmlfyq05',
            'password': '123456',
        },
    ]
}
serializer = BoolInfoModelSerializer1(data=data)
serializer.is_valid(raise_exception=True)
serializer.save()

#################################################################################
# APIView
from rest_framework.views import APIView


class BookListAPIView(APIView):
    def get(self, request):
        books = BookInfo.objects.all()
        serializer = BoolInfoModelSerializer(instance=books, many=True)
        return JsonResponse({'code': 0, 'books': serializer.data})

    def post(self, request):
        pass
