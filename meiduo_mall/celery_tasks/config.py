# _*_coding : uft-8 _*_
# @Time : 2023/4/13 10:12
# @Author : 
# @File : config
# @Project : meiduo_mall
"""
解耦：
 配置信息 key=value
 指定redis为任务队列
"""
broker_url = "redis://127.0.0.1:6379/15"  # 指定redis的15号库为celery的任务队列
# celery_result_backend = 'redis://127.0.0.1:6379/14'
