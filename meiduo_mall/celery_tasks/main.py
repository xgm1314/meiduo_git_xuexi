# _*_coding : uft-8 _*_
# @Time : 2023/4/13 10:08
# @Author : 
# @File : main
# @Project : meiduo_mall
"""
任务执行者：celery -A proj worker -l INFO
在虚拟环境下执行:celery -A实例的脚本路径 worker -l INFO
          例如:celery -A celery_tasks.main worker -l INFO
"""
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'meiduo_mall.settings')  # 为celery的运行设置django的环境

app = Celery('celery_tasks')  # 创建celery实例
# 设置broker，通过加载配置文件来设置broker
app.config_from_object('celery_tasks.config')
# 需要celery自动检测指定包的任务(autodiscover_tasks：参数是列表；列表中的元素是tasks的路径)
app.autodiscover_tasks(['celery_tasks.sms'])
