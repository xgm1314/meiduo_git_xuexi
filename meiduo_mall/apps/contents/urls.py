# _*_coding : uft-8 _*_
# @Time : 2023/4/14 13:30
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.oauth.views import QQLoginView, OauthQQView

urlpatterns = [
    path('qq/authoriztion/', QQLoginView.as_view()),
    path('oauth_callback/', OauthQQView.as_view()),

]
