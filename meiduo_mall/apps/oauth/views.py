from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse
from django.contrib.auth import login

from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall import settings
from apps.oauth.models import OauthQQUser


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
        # code = 'C40103F98B39BED1CA2DDFE12722A726'
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
            login(request, qquser.user)  # 设置session
            response = JsonResponse({'code': 0, 'errmsg': 'ok'})
            response.set_cookie('username', qquser.user.username)  # 设置cookie
            return response
