# _*_coding : uft-8 _*_
# @Time : 2023/4/19 12:19
# @Author : 
# @File : utils
# @Project : meiduo_mall

# 创建邮箱验证加密

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from meiduo_mall import settings


def generic_email_verify_token(user_id):
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600 * 24)  # 加密一天有效
    token = s.dumps({'user_id': user_id})
    return token.decode()
