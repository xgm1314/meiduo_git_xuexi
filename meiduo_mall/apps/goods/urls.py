# _*_coding : uft-8 _*_
# @Time : 2023/4/14 13:30
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.goods.views import IndexView

urlpatterns = [
    path('index/', IndexView.as_view()),
]
