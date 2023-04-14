from django.shortcuts import render

# Create your views here.
from django.views import View
from django.http import JsonResponse

from QQLoginTool.QQtool import OAuthQQ
from meiduo_mall import settings


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
