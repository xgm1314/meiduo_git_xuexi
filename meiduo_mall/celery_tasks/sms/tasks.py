# _*_coding : uft-8 _*_
# @Time : 2023/4/13 10:12
# @Author : 
# @File : tasks
# @Project : meiduo_mall
"""
生产者的任务函数
1、这个函数必须要让celery的实例的task装饰器装饰
2、需要celery自动指定包的任务
"""
from libs.yuntongxun.sms import CCP
from celery_tasks.main import app


@app.task
def celery_send_code(mobile, sms_code):
    CCP().send_template_sms(mobile, [sms_code, 5], 1)
