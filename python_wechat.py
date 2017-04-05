# _*_ coding: utf-8 _*_

"""
python_wechat.py by xianhu
主要包括如下功能：
(1) 自动提醒群红包
(2) 自动提醒关键字
(3) 自动保存被撤回消息
"""

import time
import itchat
import logging
import datetime
from itchat.content import *

# 初始化
newInstance = itchat.new_instance()
newInstance.auto_login(enableCmdQR=2)
newInstance.global_keys = ["人工智能", "机器学习", "算法", "数据挖掘"]

# 获取自己的属性字典
owner = newInstance.search_friends(name=None)

# 获取通讯录: {UserName: UserInstance}
friends = {item["UserName"]: item for item in newInstance.get_friends(update=True)}

# 消息存储队列
msg_store = {}


# 消息提取函数
def get_msg_list(msg):
    """
    提取消息内容
    """
    logging.warning("%s: %s", msg["MsgType"], msg)

    msg_id = msg["MsgId"]                   # 消息ID
    from_user_name = msg["FromUserName"]    # 消息发送者ID
    to_user_name = msg["ToUserName"]        # 消息接受者ID
    msg_type = msg["MsgType"]               # 消息类型
    msg_content = msg["Content"]            # 消息内容
    msg_file = msg["FileName"]              # 消息中所带文件的名称
    msg_time = datetime.datetime.fromtimestamp(msg["CreateTime"])  # 消息发送时间

    wind_name = msg["User"]["NickName"]     # 聊天窗口名称
    user_name = msg["ActualUserName"]       # 消息发送者的名称
    nick_name = msg["ActualNickName"] if (user_name not in friends) or (friends[user_name]["RemarkName"] == "") else friends[user_name]["RemarkName"]

    print(msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_file, msg_time, wind_name, nick_name)
    return msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_file, msg_time, wind_name, nick_name


# 消息注册，主要处理群消息
@newInstance.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    """
    消息自动接收, 接受全部的消息
    """
    # 消息提取
    msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_file, msg_time, wind_name, nick_name = get_msg_list(msg)

    # 消息存储，并删除过期消息
    msg_store[msg_id] = msg
    for _id in msg_store:
        if time.time() - msg_store[_id]["CreateTime"] > 120:
            msg_store.pop(_id)

    # 处理群消息
    if from_user_name.startswith("@@"):
        # 红包消息处理
        if msg_type == 10000 and msg_content.find("红包"):
            newInstance.send("【%s】中有红包，快抢！\nFrom: %s\nContent: %s\nTime: %s" % (wind_name, nick_name, msg_content, msg_time), toUserName="filehelper")

        # 提到自己消息处理
        if msg["IsAt"]:
            newInstance.send("【%s】中有@你的消息:\nFrom: %s\nContent: %s\nTime: %s" % (wind_name, nick_name, msg_content, msg_time), toUserName="filehelper")

        for key in newInstance.global_keys:
            if msg_content.find(key) >= 0:
                newInstance.send("【%s】中有关键字【%s】:\nFrom: %s\nContent: %s\nTime: %s" % (wind_name, key, nick_name, msg_content, msg_time), toUserName="filehelper")
                break

    # 撤回消息处理
    if msg_type == 10002 and msg_content.find("撤回"):
        old_msg_id = msg_content[msg_content.find("<msgid>")+7: msg_content.find("</msgid>")]
        msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_file, msg_time, wind_name, nick_name = get_msg_list(msg_store[old_msg_id])
        newInstance.send("【%s】中有消息被撤回:\nFrom: %s\nContent: %s\nFile: %s\nTime: %s" % (wind_name, nick_name, msg_content, msg_file, msg_time), toUserName="filehelper")
        if msg_file:
            msg_store[old_msg_id].download(msg_file)

    return


# 运行程序
newInstance.run()
