# _*_coding : uft-8 _*_
# @Time : 2023/4/14 13:30
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.pay.views import PayUrlView

urlpatterns = [
    path('payment/<order_id>/', PayUrlView.as_view()),

]
