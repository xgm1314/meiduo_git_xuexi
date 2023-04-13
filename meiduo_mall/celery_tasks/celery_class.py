# _*_coding : uft-8 _*_
# @Time : 2023/4/12 20:43
# @Author : 
# @File : celery_class
# @Project : meiduo_mall
""" celery测试 """


class Broker(object):
    """ 任务队列 """
    broker_list = []


class Worker(object):
    """ 任务执行者 """

    def run(self, broker, func):
        if func in broker.broker_list:
            func()
        else:
            return 'error'


class Celery(object):
    """ celery处理任务队列和执行者的关系 """

    def __init__(self):
        self.broker = Broker()
        self.worker = Worker()

    def add(self, func):
        """ 添加到任务队列 """
        self.broker.broker_list.append(func)

    def work(self, func):
        """ 由celery传到执行队列 """
        self.worker.run(self.broker, func)


def send_sms_code():
    """ 添加任务到任务队列 """
    print('send_sms_code')


app = Celery()  # 创建实例对象
app.add(send_sms_code)  # 添加任务至任务队列
app.work(send_sms_code)  # 执行任务队列任务
