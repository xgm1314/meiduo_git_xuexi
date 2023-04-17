from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login
import json
import re

from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall import settings
from apps.oauth.models import OauthQQUser

from apps.users.models import User


class QQLoginView(View):
    """ 第三方登录(QQ) """

    def get(self, request):
        qq = OAuthQQ(  # 生成实例对象
            client_id=settings.QQ_CLIENT_ID,  # appid
            client_secret=settings.QQ_CLIENT_SECRET,  # appsecret
            redirect_uri=settings.QQ_REDIRECT_URI,  # 用户同意登录后，跳转的页面
            state='xxxxx'
        )
        qq_login_url = qq.get_qq_url()  # 调用对象方法生成跳转连接
        return JsonResponse({'code': 0, 'errmsg': 'ok', 'login_url': qq_login_url})  # 返回数据


class OauthQQView(View):
    """ 获取openid """

    def get(self, request):
        code = request.GET.get('code')  # 获取code
        # code = '3C444A1939D681094DF0ABAAE563A535'
        qq = OAuthQQ(  # 通过code换取token
            client_id=settings.QQ_CLIENT_ID,  # appid
            client_secret=settings.QQ_CLIENT_SECRET,  # appsecret
            redirect_uri=settings.QQ_REDIRECT_URI,  # 用户同意登录后，跳转的页面
            state='xxxxx'
        )
        token = qq.get_access_token(code)
        openid = qq.get_open_id(token)  # 通过token换取openid
        try:
            qquser = OauthQQUser.objects.get(openid=openid)  # 查找数据库中是否有改openid
        except OauthQQUser.DoesNotExist:
            # 不存在报异常
            response = JsonResponse({'code': 400, 'access_token': openid})  # 返回openid信息，返回绑定页面
            return response
        else:
            # 存在
            login(request, qquser.user)  # 设置session
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)  # 设置cookie
            return response

    def post(self, request):
        body_dict = json.loads(request.body.decode())  # 获取前端传入的数据
        # print(body_dict)
        mobile = body_dict.get('mobile')
        password = body_dict.get('password')
        sms_code = body_dict.get('sms_code')
        openid = body_dict.get('access_token')
        print(openid)
        # 验证数据
        if not re.match(r'1[345789]\d{9}', mobile):  # 校验手机号
            return JsonResponse({'code': 400, 'errmsg': '手机号格式错误'})

        sms_code_client = request.POST.get('sms_code')  # 获取传入的短信验证码
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('code')  # 连接数据库
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码已失效'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})

        try:
            user = User.objects.get(mobile=mobile)  # 查询数据库是否有该用户
        except User.DoesNotExist:
            user = User.objects.create_user(username=mobile, mobile=mobile, password=password)  # 没有用户创建用户
        else:
            OauthQQUser.objects.create(user=user, openid=openid)  # 添加绑定用户信息
        login(request, user)  # 设置session
        response = JsonResponse({'code': 0, 'errmsg': 'ok'})
        response.set_cookie('username', user.username)  # 设置cookie信息
        return response  # 返回数据