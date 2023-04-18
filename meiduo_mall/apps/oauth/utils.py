# _*_coding : uft-8 _*_
# @Time : 2023/4/18 18:36
# @Author : 
# @File : utils
# @Project : meiduo_mall

# 创建openid加密的函数方法

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadData, BadSignature, SignatureExpired
from meiduo_mall import settings


def generic_openid(openid):
    """ 数据加密 """
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    access_token = s.dumps({'openid': openid})
    return access_token.decode()  # 将bytes类型数据转换为字符串


def check_access_token(token):
    """ 数据解密 """
    s = Serializer(secret_key=settings.SECRET_KEY, expires_in=3600)
    try:
        result = s.loads(token)
    except Exception:
        return None
    else:
        return result.get('openid')  # 获取加密的openid
