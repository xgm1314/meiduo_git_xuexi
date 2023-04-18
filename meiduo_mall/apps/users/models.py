from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ 用户表 """
    mobile = models.CharField(verbose_name='手机号', max_length=11, unique=True)
    email_active = models.BooleanField(verbose_name='邮箱激活状态', default=False, )

    class Meta:
        db_table = 'tb_users'
        verbose_name = '用户管理'
        verbose_name_plural = verbose_name
