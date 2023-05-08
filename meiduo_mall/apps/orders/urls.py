# _*_coding : uft-8 _*_
# @Time : 2023/4/14 13:30
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.orders.views import OrderSettlementView, OrderCommitView

urlpatterns = [
    path('orders/settlement/', OrderSettlementView.as_view()),
    path('orders/commit/', OrderCommitView.as_view()),

]
