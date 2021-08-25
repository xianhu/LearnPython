# _*_ coding: utf-8 _*_

"""
测试
"""

import time
from python_celery import add

if __name__ == "__main__":
    result = []
    for i in range(10):
        result.append(add.delay(1, 2))
    print("----", time.time())
    for i in result:
        print(i, i.get())
    print("----", time.time())