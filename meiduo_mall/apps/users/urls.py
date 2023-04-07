# _*_coding : uft-8 _*_
# @Time : 2023/4/6 22:03
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.users.views import UsernameCountView

urlpatterns = [
    path('username/<username:username>/count/', UsernameCountView.as_view()),
]
