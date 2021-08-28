# _*_ coding: utf-8 _*_

"""
测试celery
运行：celery -A celery1:app worker -l INFO
"""

import time
from celery import Celery

broker = 'redis://152.136.149.221:9002/10'   # 用redis做broker，中间件
backend = 'redis://152.136.149.221:9002/11'    # 用redis做broken，用来保存结果

app = Celery('tasks',broker=broker,backend=backend)

@app.task
def add(x, y):
    print(time.time(), x, y)
    time.sleep(3)
    print(time.time(), x, y, "--")
    return x + y
