from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.views import View
from apps.users.models import User
import re


class UsernameCountView(View):
    def get(self, request, username):
        # if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名已存在'})
        count = User.objects.filter(username=username).count()
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})
