# _*_coding : uft-8 _*_
# @Time : 2023/4/6 22:27
# @Author : 
# @File : converters
# @Project : meiduo_mall
from django.urls import converters


class UsernameConverter:
    regex = '[a-zA-Z0-9_-]{5,20}'

    def to_python(self, value):
        return value
