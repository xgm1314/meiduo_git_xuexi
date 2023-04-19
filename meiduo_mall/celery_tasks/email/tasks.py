# _*_coding : uft-8 _*_
# @Time : 2023/4/19 19:21
# @Author : 
# @File : tasks
# @Project : meiduo_mall

# 创建email的celery方法

import logging
from django.core.mail import send_mail
from celery_tasks.main import app

# logger = logging.getLogger("django")


@app.task()
def celery_send_email(subject, message, from_email, recipient_list, html_message):
    # from time import sleep
    # sleep(20)
    send_mail(
        subject=subject,
        message=message,
        from_email=from_email,
        recipient_list=recipient_list,
        html_message=html_message)
