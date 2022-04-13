# _*_ coding: utf-8 _*_

"""
测试
"""

import time

from python_celery import add

if __name__ == "__main__":
    result = []
    for i in range(10):
        result.append(add.delay(i, i))
    print("----", time.time())
    for index, item in enumerate(result):
        print(index, item.get())
    print("----", time.time())
