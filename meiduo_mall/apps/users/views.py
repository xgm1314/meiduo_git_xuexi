from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.views import View
from apps.users.models import User


class UsernameCountView(View):
    def get(self, request, username):
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': '用户已存在'})
