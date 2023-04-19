# _*_coding : uft-8 _*_
# @Time : 2023/4/6 22:27
# @Author : 
# @File : converters
# @Project : meiduo_mall
from django.urls import converters


class UsernameConverter:
    ''' 用户名验证 '''
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return value


class UserMobileConverter:
    ''' 手机号验证 '''
    regex = '1[345789]\d{9}'

    def to_python(self, value):
        return value


class EmailMobileConverter:
    ''' 邮箱校验 '''
    regex = '^[a-zA-Z0-9_.-]+@[a-zA-Z0-9-]+(\.[a-zA-Z0-9-]+)*\.[a-zA-Z0-9]{2,6}$'

    def to_python(self, value):
        return value
