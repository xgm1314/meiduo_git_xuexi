# _*_coding : uft-8 _*_
# @Time : 2023/4/6 22:03
# @Author : 
# @File : urls
# @Project : meiduo_mall
from django.urls import path
from apps.users.views import UsernameCountView, UserMobileCountView, RegisterView, LoginView, LogoutView, CenterView, \
    EmailView, EmailVerifyView, AddressCreateView, AddressView

urlpatterns = [
    path('username/<username:username>/count/', UsernameCountView.as_view()),
    path('mobile/<mobile:mobile>/count/', UserMobileCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('info/', CenterView.as_view()),
    path('emails/', EmailView.as_view()),
    path('emails/verification/', EmailVerifyView.as_view()),
    path('addresses/create/', AddressCreateView.as_view()),
    path('addresses/', AddressView.as_view()),
]
