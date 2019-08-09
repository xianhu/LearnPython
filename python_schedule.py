# _*_ coding: utf-8 _*_

"""
调度的使用
"""

import time
import datetime
from threading import Timer
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler


def print_hello():
    print("TimeNow in func: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    return


if __name__ == "__main__":
    # 1. 使用Threading模块中的Timer
    # t = Timer(2, print_hello)
    #
    # print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # t.start()
    # print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # exit()

    # 2. BlockingScheduler：在进程中运行单个任务，调度器是唯一运行的东西, 采用阻塞的方式
    scheduler = BlockingScheduler()

    # 采用固定时间间隔（interval）的方式，每隔5秒钟执行一次
    scheduler.add_job(print_hello, "interval", seconds=5)

    # 采用date的方式，在特定时间只执行一次
    # scheduler.add_job(print_hello, "date", run_date=datetime.datetime.now() + datetime.timedelta(seconds=5))

    # print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # scheduler.start()
    # print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # exit()

    # 3. BackgroundScheduler: 适合于要求任何在程序后台运行的情况，当希望调度器在应用后台执行时使用。采用非阻塞的方式
    scheduler = BackgroundScheduler()

    # 采用固定时间间隔（interval）的方式，每隔3秒钟执行一次
    scheduler.add_job(print_hello, "interval", seconds=5)

    # 这是一个独立的线程
    # print("TimeNow start: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # scheduler.start()
    # print("TimeNow end: %s" % (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    # while True:
    #     time.sleep(2)
