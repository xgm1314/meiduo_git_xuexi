from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.
from django.views import View
from apps.users.models import User
import re
import json


class UsernameCountView(View):
    ''' 用户名验证 '''

    def get(self, request, username):
        # if not re.match('[a-zA-Z0-9_-]{5,20}', username):
        #     return JsonResponse({'code': 200, 'errmsg': '用户名已存在'})
        count = User.objects.filter(username=username).count()
        if count > 0:
            return JsonResponse({'code': 400, 'count': count, 'errmsg': '用户已存在'})
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class UserMobileCountView(View):
    ''' 手机号验证 '''

    def get(self, request, mobile):
        count = User.objects.filter(mobile=mobile).count()
        # print(count)
        if count > 0:
            return JsonResponse({'code': 400, 'count': count, 'errmsg': '手机号已存在'})
        return JsonResponse({'code': 0, 'count': count, 'errmsg': 'ok'})


class RegisterView(View):
    ''' 用户注册 '''

    def post(self, request):
        # 接受收据JSON
        body_bytes = request.body
        body_str = body_bytes.decode()
        # print(body_str)
        body_dict = json.loads(body_str)
        # print(body_dict)
        # 获取数据
        username = body_dict.get('username')
        password = body_dict.get('password')
        password2 = body_dict.get('password2')
        mobile = body_dict.get('mobile')
        allow = body_dict.get('allow')
        # print(allow)
        # 3. 验证数据
        #     3.1 用户名，密码，确认密码，手机号，是否同意协议 都要有
        # all([xxx,xxx,xxx])
        # all里的元素 只要是 None,False
        # all 就返回False，否则返回True

        if not all([username, password, password2, mobile]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        #     3.2 用户名满足规则，用户名不能重复
        if not re.match('[a-zA-Z_-]{5,20}', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名不满足规则'})
        count_username = User.objects.filter(username=username).count()
        if count_username > 0:
            return JsonResponse({'code': 400, 'errmsg': '用户已存在'})
        #     3.3 密码满足规则
        #     3.4 确认密码和密码要一致
        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '密码不一致'})
        #     3.5 手机号满足规则，手机号也不能重复
        if not re.match(r'1[345789]\d{9}', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号格式错误'})
        count_mobile = User.objects.filter(mobile=mobile).count()
        # print(count)
        if count_mobile > 0:
            return JsonResponse({'code': 400, 'errmsg': '手机号已存在'})
        #     3.6 需要同意协议
        if not allow:
            return JsonResponse({'code': 400, 'errmsg': '请勾选同意协议'})
        # # 添加用户方式一(密码未加密):
        # user = User(username=username, password=password, mobile=mobile)
        # user.save()
        # # 添加用户方式二(密码未加密):
        # User.objects.create(username=username, password=password, mobile=mobile)
        # 添加加密密码用户
        user = User.objects.create_user(username=username, password=password, mobile=mobile)
        # 添加session数据(django提供的状态保持方法)
        from django.contrib.auth import login
        login(request, user)
        return JsonResponse({'code': 0, 'errmsg': 'ok'})


class LoginView(View):
    """ 用户登录 """

    def post(self, request):
        # 接受数据
        body_str = request.body.decode()
        body_dict = json.loads(body_str)
        username = body_dict.get('username')
        password = body_dict.get('password')
        remembered = body_dict.get('remembered')
        # 验证数据
        if not all([username, password]):
            return JsonResponse({'code': 400, 'errmsg': '请填写用户名或密码'})

        # 验证是以账号登录还是手机号登录
        # 可以根据修改User.USERNAME_FIELD字段来影响authenticate的查询
        if re.match(r'1[345789]\d{9}', username):
            User.USERNAME_FIELD = 'mobile'
        else:
            User.USERNAME_FIELD = 'username'

        # 验证账号或者密码是否正确
        from django.contrib.auth import authenticate
        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({'code': 400, 'errmsg': '用户名或密码错误'})
        # session
        from django.contrib.auth import login
        login(request, user)
        # 判断是否记住登录
        if remembered:
            request.session.set_expiry(60 * 60 * 24 * 7)  # 7天免登录
        else:
            request.session.set_expiry(0)  # 关闭会话session清空

        # 利用cookie登录信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', username)
        return response


class LogoutView(View):
    """ 退出登录 """

    def delete(self, request):
        from django.contrib.auth import logout
        logout(request)  # 退出登录，清除session信息
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.delete_cookie('username')  # 清楚cookie信息
        return response


from utils.views import LoginRequiredJSONMixin


class CenterView(LoginRequiredJSONMixin, View):
    """ 用户中心 """

    def get(self, request):
        return JsonResponse({'code': 0, 'errmsg': 'ok'})
