
###########################################################
"""
drf 框架 能够帮助我们实现  序列化和反序列化的功能  (对象和字典的相互转换)


BookInfo(对象)        ---序列化器类--->             字典

豆子                  ---豆浆机--->              豆浆


序列化器类
    ① 将对象转换为字典


序列化器类的定义
    ① 参考模型来定义就可以了


class 序列化器名字(serializers.Serializer):
    字段名=serializer.类型(选项)


    字段名和模型字段名一致
    字段的类型和模型的类型一致

"""
from rest_framework import serializers

class BookInfoSerializer(serializers.Serializer):

    id =serializers.IntegerField()
    name =serializers.CharField()
    pub_date =serializers.DateField()
    readcount =serializers.IntegerField()


################定义人物模型对应的序列化器#####################
class PeopleInfoSerializer(serializers.Serializer):

    id=serializers.IntegerField()
    name=serializers.CharField()
    password=serializers.CharField()
    description=serializers.CharField()
    is_delete=serializers.BooleanField()

    ###对外键进行学习
    # ①  如果我们定义的序列化器外键字段类型为 IntegerField
    # 那么,我们定义的序列化器字段名 必须和数据库中的外键字段名一致
    book_id=serializers.IntegerField()
