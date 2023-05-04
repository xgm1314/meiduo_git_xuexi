# _*_coding : uft-8 _*_
# @Time : 2023/4/14 13:30
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.carts.views import CartView, CartsSelect

urlpatterns = [
    path('carts/', CartView.as_view()),
    path('carts/select/', CartsSelect.as_view()),

]
