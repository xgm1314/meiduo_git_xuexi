#####################序列化######################################
"""
drf 框架 能够帮助我们实现  序列化和反序列化的功能  (对象和字典的相互转换)


BookInfo(对象)        ---序列化器类--->             字典

豆子                  ---豆浆机--->              豆浆


序列化器类
    ① 将对象转换为字典
    ② 将字典转换为对象  -- 反序列化


序列化器类的定义
    ① 参考模型来定义就可以了


class 序列化器名字(serializers.Serializer):
    字段名=serializer.类型(选项)


    字段名和模型字段名一致
    字段的类型和模型的类型一致

"""
from rest_framework import serializers


class PeopleRelatedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()


class BookInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(write_only=True, max_length=10, min_length=5)  # 设置字段的最大长度和最小长度
    pub_date = serializers.DateField(required=True)
    readcount = serializers.IntegerField(required=True)
    commentcount = serializers.IntegerField(required=True)

    # 单个参数验证
    def validate_readcount(self, value):
        """ 判断数据类型是否满足(方法验证数据) """
        if value < 0:
            # raise Exception('阅读量不能为负数')
            raise serializers.ValidationError('阅读量不能为负数~~~')  # 模拟系统抛出异常
        return value

    # 多个参数验证
    def validate(self, attrs):  # attrs 就是传入的data字典
        readcount = attrs.get('readcount')
        commentcount = attrs.get('commentcount')
        if readcount < commentcount:
            raise serializers.ValidationError('评论量不能大于阅读量')
        return attrs

    def create(self, validated_data):  # validated_data 是传入的data字典数据
        """ 验证数据没有问题，保存到数据库 """
        return BookInfo.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """ 验证数据没有问题，更新到数据库 """
        # instance 序列化器创造时，传递的对象
        # validated_data 序列化器创造时，验证没问题的数据
        instance.name = validated_data.get('name', instance.name)
        instance.pub_date = validated_data.get('pub_date', instance.pub_date)
        instance.readcount = validated_data.get('readcount', instance.readcount)
        instance.commentcount = validated_data.get('commentcount', instance.commentcount)
        instance.save()  # 保存到数据库
        return instance

    #
    # people = PeopleRelatedSerializer(many=True)
    """
    {
     'id': 1, 'name': '射雕英雄传', 'pub_date': '1980-05-01', 'readcount': 12,
     'people': [
                    OrderedDict([('id', 1), ('name', '郭靖'), ('passwor3456abc')]), 
                    OrderedDict([('id', 2), ('name', '黄蓉'), ('password', '123456abc')]),
                    OrderedDict([('id', 3), ('name', '黄药师'), ('passwor123456abc')]), 
                    OrderedDict([('id', 4), ('name', '欧阳锋'), ('password', '123456abc')]), 
                    OrderedDict([('id', 5), ('name', '梅超风'), ('pas, '123456abc')])
                ]
    }

    """


################定义人物模型对应的序列化器#####################
from book.models import BookInfo


class PeopleInfoSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    password = serializers.CharField()
    description = serializers.CharField()
    is_delete = serializers.BooleanField()

    ###对外键进行学习
    # ①  如果我们定义的序列化器外键字段类型为 IntegerField
    # 那么,我们定义的序列化器字段名 必须和数据库中的外键字段名一致
    # book_id=serializers.IntegerField()

    # ② 如果我们期望的外键数据的key就是模型字段的名字,那么 PrimaryKeyRelatedField 就可以获取到关联的模型id值
    # queryset 在验证数据的时候,我们要告诉系统,在哪里匹配外键数据
    # book=serializers.PrimaryKeyRelatedField(queryset=BookInfo.objects.all())
    # 或者
    # read_only=True 意思就是 我不验证数据了
    # book=serializers.PrimaryKeyRelatedField(read_only=True)

    # ③ 如果我们期望获取外键关联的 字符串的信息, 这个时候 我们可以使用 StringRelationField
    # book=serializers.StringRelatedField()

    # ④ 如果我们期望获取, book 所关联的模型的 所有数据,这个时候我们就定义 book=BookInfoSerializer()
    # book=关联的BookInfo的一个关联对象数据
    # book=BookInfo.objects.get(id=xxx)

    # book=BookInfoSerializer(instance=book).data
    # 等号右边的 book 是模型对象
    # 等号左边的book 是字典数据
    # book=BookInfoSerializer()
    """
    {
    'id': 1, 'name': '郭靖', 'password': '123456abc', 'description': '降龙十八掌', 'is_delete': False, 
    'book': OrderedDict([('id', 1), ('name','射雕英雄传'), ('pub_date', '1980-05-01'), ('readcount', 12)])
    }

    """


"""

①book:1                             PrimaryKeyRelationField                                                       

②book_id:1                          IntergerField

③book:射雕英雄传                      StringRelationField

④book: {id:1,name:射雕英雄传,readcount:10}   BookInfoSerializer


"""


class BoolInfoModelSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=10, min_length=5, required=True)  # 当自动生成的选项不满足时，可以重写

    class Meta:
        model = BookInfo  # ModelSerializer必须设置model
        fields = '__all__'  # 设置自动生成的字段列表__all__ 表示所有字段
        # fields=['id','name']#设置需要生成的字段
        # exclude = ['id', 'name']  # 设置除了列表中的字段，其他字段都生成

        # extra_kwargs = {  # 当自动生成的选项不满足时，重新设置选项
        #     # '字段名':{'选项名':value,}
        #     'name': {
        #         'max_length': 40,
        #         'min_length': 10
        #     }
        # }


from book.models import PeopleInfo


class PeopleInfoModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PeopleInfo
        fields = ['id', 'name', 'book', 'password', 'is_delete', 'description']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'is_delete': {
                'read_only': True
            },
        }


class PeopleInfoModelSerializer1(serializers.ModelSerializer):
    book_id = serializers.IntegerField(required=False)  # 在序列化嵌套时，因为book_id没有外键，所以需要先增加required=False

    class Meta:
        model = PeopleInfo
        fields = ['id', 'name', 'book_id', 'password', 'is_delete', 'description']
        extra_kwargs = {
            'password': {
                'write_only': True
            },
            'is_delete': {
                'read_only': True
            },
        }


class BoolInfoModelSerializer1(serializers.ModelSerializer):
    """ 序列化器嵌套 """
    people = PeopleInfoModelSerializer1(many=True)

    class Meta:
        model = BookInfo
        fields = '__all__'

    """
    序列化器嵌套序列化器写入数据的时候.默认系统是不支持写入的
    我们需要自己实现create方法 来实现数据的写入

    validate:
    data={
        'name':'离离原上草',

    }

    people 
    'people':[
            {
                'name': '靖妹妹111',
                'password': '123456abc'
            },
            {
                'name': '靖表哥222',
                'password': '123456abc'
            }
        ]

    写入数据的思想是:  因为 当前 书籍和人物的关系是 1对多  应该先写入 1的模型数据,再写入 多的模型数据

    data.pop('people')  'name':'离离原上草',

    people 再写入 people列表数据

    """

    def create(self, validated_data):
        people = validated_data.pop('people')  # 把validated_data的嵌套数据分解开
        # print(people)
        book = BookInfo.objects.create(**validated_data)  # 写入书籍信息
        for item in people:  # 对字典列表进行遍历
            PeopleInfo.objects.create(book=book, **item)
        return book
