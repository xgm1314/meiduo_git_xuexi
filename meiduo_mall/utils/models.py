# _*_coding : uft-8 _*_
# @Time : 2023/4/14 12:36
# @Author : 
# @File : models
# @Project : meiduo_mall
from django.db import models


class BaseModels(models.Model):
    """ 定义基类 补充时间字段 """
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True)

    class Meta:
        abstract = True  # 说明是抽象模型类，用于继承使用，数据库迁移时不会创建BaseModels的表
