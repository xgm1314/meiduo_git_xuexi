"""meiduo_mall URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

"""
from django.http import HttpResponse


def log(request):
    import logging  # 导入日志模块
    logger = logging.getLogger('django')  # 创建日志器(在settings里有设置)
    logger.info('信息记录')  # 调用日志器的方法保存日志
    logger.warning('警告信息')
    logger.error('错误信息')
    logger.debug('调试')
    return HttpResponse('log')
"""

# 注册转换器
from utils.converters import UsernameConverter,UserMobileConverter
from django.urls import register_converter

register_converter(UsernameConverter, 'username')
register_converter(UserMobileConverter, 'mobile')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.users.urls')),
    path('', include('apps.verifications.urls')),
    path('', include('apps.oauth.urls')),
    path('', include('apps.areas.urls')),
    path('', include('apps.goods.urls')),
    path('', include('apps.contents.urls')),
    path('', include('apps.carts.urls')),
]
