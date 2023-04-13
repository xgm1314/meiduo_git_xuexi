# _*_coding : uft-8 _*_
# @Time : 2023/4/13 19:51
# @Author : 
# @File : views
# @Project : meiduo_mall
"""
判断用户是否登录组件，返回JSON数据
"""
from django.http import JsonResponse
from django.contrib.auth.mixins import AccessMixin, LoginRequiredMixin


# class LoginRequiredJSONMixin(AccessMixin):
#     # 方式一：
#     """Verify that the current user is authenticated."""
#
#     def dispatch(self, request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             return JsonResponse({'code': 400, 'errmsg': '用户未登录,请登录'})
#         return super().dispatch(request, *args, **kwargs)


class LoginRequiredJSONMixin(LoginRequiredMixin):
    # 方式二：
    def handle_no_permission(self):
        return JsonResponse({'code': 400, 'errmsg': '用户未登录,请登录'})
