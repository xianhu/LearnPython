# _*_ coding: utf-8 _*_

"""
Python操作Redis实现消息的发布与订阅
"""

import sys
import time
import redis

# 全局变量
conn_pool = redis.ConnectionPool(host="localhost", port=6379, db=1)
conn_inst = redis.Redis(connection_pool=conn_pool)
channel_name = "fm-101.1"


def public_test():
    while True:
        # 发布消息
        conn_inst.publish(channel_name, "hello " + str(time.time()))
        if int(time.time()) % 10 == 1:
            conn_inst.publish(channel_name, "over")
        time.sleep(1)


def subscribe_test(_type=0):
    pub = conn_inst.pubsub()
    pub.subscribe(channel_name)

    if _type == 0:
        # 订阅消息
        for item in pub.listen():
            print("Listen on channel: %s" % item)
            if item["type"] == "message" and item["data"].decode() == "over":
                print(item["channel"].decode(), "已停止发布")
                break
    else:
        # 另一种订阅模式
        while True:
            item = pub.parse_response()
            print("Listen on channel: %s" % item)
            if item[0].decode() == "message" and item[2].decode() == "over":
                print(item[1].decode(), "已停止发布")
                break

    # 取消订阅
    pub.unsubscribe()
    return


if __name__ == '__main__':
    if sys.argv[1] == "public":
        public_test()
    else:
        subscribe_test(int(sys.argv[2]))
