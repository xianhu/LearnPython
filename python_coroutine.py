# _*_ coding: utf-8 _*_

"""
python_coroutine.py by xianhu
"""

import asyncio
import aiohttp
import threading


# 生产者、消费者例子
def consumer():         # 定义消费者，由于有yeild关键词，此消费者为一个生成器
    print("[Consumer] Init Consumer ......")
    r = "init ok"       # 初始化返回结果，并在启动消费者时，返回给生产者
    while True:
        n = yield r     # 消费者通过yield关键词接收生产者产生的消息，同时返回结果给生产者
        print("[Consumer] conusme n = %s, r = %s" % (n, r))
        r = "consume %s OK" % n     # 消费者消费结果，下个循环返回给生产者


def produce(c):         # 定义生产者，此时的 c 为一个生成器
    print("[Producer] Init Producer ......")
    r = c.send(None)    # 启动消费者生成器，同时第一次接收返回结果
    print("[Producer] Start Consumer, return %s" % r)
    n = 0
    while n < 5:
        n += 1
        print("[Producer] While, Producing %s ......" % n)
        r = c.send(n)   # 向消费者发送消息，同时准备接收结果。此时会切换到消费者执行
        print("[Producer] Consumer return: %s" % r)
    c.close()           # 关闭消费者生成器
    print("[Producer] Close Producer ......")

# produce(consumer())


# 异步IO例子：适配Python3.4，使用asyncio库
@asyncio.coroutine
def hello(index):                   # 通过装饰器asyncio.coroutine定义协程
    print('Hello world! index=%s, thread=%s' % (index, threading.currentThread()))
    yield from asyncio.sleep(1)     # 模拟IO任务
    print('Hello again! index=%s, thread=%s' % (index, threading.currentThread()))@asyncio.coroutine

loop = asyncio.get_event_loop()     # 得到一个事件循环模型
tasks = [hello(1), hello(2)]        # 初始化任务列表
loop.run_until_complete(asyncio.wait(tasks))    # 执行任务
loop.close()                        # 关闭事件循环列表


# 异步IO例子：适配Python3.5，使用async和await关键字
async def hello1(index):            # 通过关键字async定义协程
    print('Hello world! index=%s, thread=%s' % (index, threading.currentThread()))
    await asyncio.sleep(1)          # 模拟IO任务
    print('Hello again! index=%s, thread=%s' % (index, threading.currentThread()))

loop = asyncio.get_event_loop()     # 得到一个事件循环模型
tasks = [hello1(1), hello1(2)]      # 初始化任务列表
loop.run_until_complete(asyncio.wait(tasks))    # 执行任务
loop.close()                        # 关闭事件循环列表


# aiohttp 实例
async def get(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(url, resp.status)
            print(url, await resp.text())

loop = asyncio.get_event_loop()     # 得到一个事件循环模型
tasks = [                           # 初始化任务列表
    get("http://zhushou.360.cn/detail/index/soft_id/3283370"),
    get("http://zhushou.360.cn/detail/index/soft_id/3264775"),
    get("http://zhushou.360.cn/detail/index/soft_id/705490")
]
loop.run_until_complete(asyncio.wait(tasks))    # 执行任务
loop.close()                        # 关闭事件循环列表
