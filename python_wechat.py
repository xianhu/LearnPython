# _*_ coding: utf-8 _*_

"""
python_wechat.py by xianhu
主要包括如下功能：
(1) 自动提醒群红包
(2) 自动提醒关键字
(3) 自动保存被撤回消息
"""

import re
import time
import itchat
import logging
import datetime
from itchat.content import *

# 初始化
newInstance = itchat.new_instance()
newInstance.auto_login(hotReload=False, enableCmdQR=2)
newInstance.global_keys = ["人工智能", "机器学习", "算法", "数据挖掘"]
newInstance.to_user_name = "filehelper"

# 获取自己的属性字典：UserName, NickName, RemarkName, Sex(1 or 2)
newInstance.owner = newInstance.loginInfo["User"]

# 获取通讯录: {UserName: UserInstance}
newInstance.friends = {user["UserName"]: user for user in newInstance.get_friends(update=True)}

# 消息存储队列
newInstance.msg_store = {}


# 消息提取函数
def get_msg_list(msg):
    """
    提取消息内容
    """
    logging.warning("%s", msg)

    msg_id = msg["MsgId"]                       # 消息ID
    from_user_name = msg["FromUserName"]        # 消息发送者ID
    to_user_name = msg["ToUserName"]            # 消息接受者ID

    msg_type = msg["MsgType"]                   # 消息类型
    msg_content = msg["Content"]                # 消息内容
    msg_time = datetime.datetime.fromtimestamp(msg["CreateTime"])  # 消息发送时间

    msg_file = msg["FileName"]                  # 消息中所带文件的名称
    msg_url = msg["Url"]                        # 消息中带有的链接地址

    if from_user_name.startswith("@@"):
        # 群消息
        wind_name = msg["User"]["RemarkName"] if msg["User"]["RemarkName"] else msg["User"]["NickName"]
        nick_name = msg["ActualNickName"] if (msg["ActualUserName"] not in newInstance.friends) or \
                                             (not newInstance.friends[msg["ActualUserName"]]["RemarkName"]) else newInstance.friends[msg["ActualUserName"]]["RemarkName"]
    else:
        # 个人消息
        wind_name = msg["User"]["RemarkName"] if msg["User"]["RemarkName"] else msg["User"]["NickName"]
        nick_name = wind_name

    we_type = msg["Type"]                       # 消息类型
    we_text = msg["Text"]                       # 消息内容

    return msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_url, wind_name, nick_name, we_type, we_text


# 消息注册，主要处理群消息
@newInstance.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    """
    消息自动接收, 接受全部的消息
    """
    # 消息提取
    msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_url, wind_name, nick_name, we_type, we_text = get_msg_list(msg)

    # 消息过滤，过滤自己发送的消息
    if from_user_name == newInstance.owner["UserName"]:
        logging.warning("message from myself, skip")
        return

    # 消息过滤, 只监测文字、注解、分享、图片、语音、视频、附件等
    if we_type not in ["Text", "Note", "Sharing", "Picture", "Recording", "Video", "Attachment"]:
        logging.warning("message ignored")
        return

    if we_type in ["Picture", "Recording", "Video", "Attachment"]:
        re_length = re.search("[\"\s]length=\"(?P<length>[\d]+?)\"", msg_content, flags=re.IGNORECASE)
        if (not msg_content) or (re_length and (int(re_length.group("length")) < 5000000)):
            we_text(".Cache/" + msg_file)
            logging.warning("downloading %s to .Cache/", msg_file)

    # 消息存储
    newInstance.msg_store[msg_id] = msg

    # 删除过期消息
    ids_list = [_id for _id in newInstance.msg_store if time.time() - newInstance.msg_store[_id]["CreateTime"] > 120]
    for _id in ids_list:
        logging.warning("delete message, message_id = %s", _id)
        newInstance.msg_store.pop(_id)

    # 处理群消息
    if from_user_name.startswith("@@"):
        # 红包消息处理
        if we_type == "Note" and we_text.find("收到红包，请在手机上查看") >= 0:
            newInstance.send("【%s】中有红包，快抢！\nFrom: %s\nContent: %s\nTime: %s" % (wind_name, nick_name, msg_content, msg_time), toUserName=newInstance.to_user_name)

        # 提到自己消息处理
        if msg["IsAt"]:
            newInstance.send("【%s】中有@你的消息:\nFrom: %s\nContent: %s\nTime: %s" % (wind_name, nick_name, msg_content, msg_time), toUserName=newInstance.to_user_name)

        for key in newInstance.global_keys:
            if msg_content.find(key) >= 0:
                newInstance.send("【%s】中有关键字【%s】:\nFrom: %s\nContent: %s\nTime: %s" % (wind_name, key, nick_name, msg_content, msg_time), toUserName=newInstance.to_user_name)
                break

    # 撤回消息处理
    if we_type == "Note" and we_text.find("撤回了一条消息") >= 0:
        old_msg = newInstance.msg_store.get(msg_content[msg_content.find("<msgid>")+7: msg_content.find("</msgid>")])
        if not old_msg:
            return

        msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_url, wind_name, nick_name, we_type, we_text = get_msg_list(old_msg)
        if we_type in ["Picture", "Recording", "Video", "Attachment"]:
            msg_content = msg_file
        elif we_type == "Sharing":
            msg_content = we_text + ": " + msg_url

        newInstance.send("【%s】中有消息被撤回:\nFrom: %s\nType: %s\nContent: %s\nTime: %s" % (wind_name, nick_name, we_type, msg_content, msg_time), toUserName=newInstance.to_user_name)
    return


# 运行程序
newInstance.run()
