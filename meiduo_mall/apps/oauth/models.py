from django.db import models

# Create your models here.
from utils.models import BaseModels


class OauthQQUser(BaseModels):
    """ QQ用户登录 """
    user = models.ForeignKey(verbose_name='用户', to='users.User', on_delete=models.CASCADE)
    openid = models.CharField(verbose_name='openid', max_length=64, db_index=True)

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'qq用户登录数据'
        verbose_name_plural = verbose_name
