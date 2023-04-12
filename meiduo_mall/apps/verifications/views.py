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

    def get_send(self, request, mobile):
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
        if 'send_flag_%s' % mobile is not None:  # 判断是否有发送短信的标记
            return JsonResponse({'code': 400, 'errmsg': '操作过于频繁,请勿频繁操作'})
        from random import randint
        sms_code = '%04d' % randint(0, 9999)  # 生成4位随机验证码
        redis_cli.setex(mobile, 120, sms_code)  # 保存验证码
        redis_cli.setex('send_flag_%s' % mobile, 60, 1)  # 发送短信后,标记发送短信的标记
        from libs.yuntongxun.sms import CCP
        CCP().send_template_sms('17854157598', [sms_code, 2], 1)  # 发送验证码
        return JsonResponse({'code': 0, 'errmsg': '验证码发送成功'})  # 返回响应

    def get_receive(self, request, mobile):
        sms_code_client = request.POST.get('sms_code')  # 获取传入的短信验证码
        from django_redis import get_redis_connection
        redis_conn = get_redis_connection('code')  # 连接数据库
        sms_code_server = redis_conn.get('sms_%s' % mobile)
        if not sms_code_server:
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})
        if sms_code_client != sms_code_server.decode():
            return JsonResponse({'code': 400, 'errmsg': '短信验证码有误'})
        return JsonResponse({'code': 0, 'errmsg': '验证成功'})  # 返回响应
