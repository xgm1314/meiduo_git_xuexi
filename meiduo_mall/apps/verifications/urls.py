# _*_coding : uft-8 _*_
# @Time : 2023/4/10 20:05
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.verifications.views import ImageCodeView, SmsCodeView

urlpatterns = [
    path('image_codes/<uuid>/', ImageCodeView.as_view()),
    path('sms_codes/<mobile>/', SmsCodeView.as_view()),

]
