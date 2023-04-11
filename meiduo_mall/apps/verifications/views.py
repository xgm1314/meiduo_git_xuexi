from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
# Create your views here.
from django.views import View


class ImageCodeView(View):
    ''' 图片验证码 '''

    def get(self, request, uuid):
        from libs.captcha.captcha.captcha import captcha
        text, image = captcha.generate_captcha()  # 生成图片验证码和图片二进制
        from django_redis import get_redis_connection
        # 通过redis把图片验证码保存起来
        redis_cli = get_redis_connection('code')  # 连接redis数据库
        redis_cli.setex(uuid, 120, text)  # 设置redis的key,value,过期时间
        # 返回图片二进制，图片二进制用HttpResponse，返回数据需要用参数content_type参数
        return HttpResponse('image', content_type='image/jpeg')


class SmsCodeView(View):
    ''' 短信验证码 '''

    def get(self, request, mobile):
        # 获取请求参数
        image_code = request.GET.get('image_code')
        uuid = request.GET.get('image_code_id')
        # 验证参数
        if not all([image_code, uuid]):
            return JsonResponse({'code': 400, 'errmsg': '参数不全'})
        # 验证图片验证码
        from django_redis import get_redis_connection
        redis_cli = get_redis_connection('code')  # 连接redis库
        redis_image_code = redis_cli.get('uuid')  # 获取redis库的值
        if redis_image_code is None:  # 如果不存在
            return JsonResponse({'code': 400, 'errmsg': '图片验证码已过期'})
        if redis_image_code.decode().lower() != image_code.lower():  # 全部转换成小写进行对比
            return JsonResponse({'code': 400, 'errmsg': '图片验证码错误'})
        from random import randint
        sms_code = '%04d' % randint(0, 9999)  # 生成4位随机验证码
        redis_cli.setex(mobile, 120, sms_code)  # 保存验证码
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms('17854157598', [sms_code, 2], 1)  # 发送验证码
        return JsonResponse({'code': 0, 'errmsg': 'ok'})  # 返回响应
