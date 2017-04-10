# _*_ coding: utf-8 _*_

"""
python_wechat.py by xianhu
主要包括如下功能：
(1) 自动提醒群红包
(2) 自动提醒群中@自己或@all的内容
(3) 自动提醒群中带有特殊关键字的消息
(4) 自动保存被撤回消息，包括内容、文件、图片、语音、视频等
"""

import re
import time
import itchat
import logging
import datetime
from itchat.content import *

# 初始化
my = itchat.new_instance()
my.auto_login(hotReload=False, enableCmdQR=2)
my.global_keys = ["人工智能", "机器学习", "算法", "数据挖掘"]
my.to_user_name = "filehelper"

# my还包括的以下属性，注意用点.查看：
# (1) alive 是否还活着，isLogging 是否已登陆
# (2) loginInfo 登陆信息，其中的User属性为自己的信息User字典类，包括UserName, NickName, RemarkName, Sex(1 or 2)等
# (3) memberList 通讯录列表，每一项为一个User字典类
# (4) chatroomList 群聊列表，每一项为一个Chatroom字典类，包括UserName, NickName, RemarkName, MemberCount等
# (5) mpList 订阅号列表，每一项为一个MassivePlatform字典类，包括UserName, NickName等

# 获取并更新通讯录: {UserName: UserInstance}
my.friends = {user["UserName"]: user for user in my.get_friends(update=True)}

# 消息存储队列
my.msg_store = {}


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

    wind_name = msg["User"]["RemarkName"] if msg["User"].get("RemarkName") else (
        msg["User"]["NickName"] if msg["User"].get("NickName") else to_user_name
    )

    if from_user_name.startswith("@@"):
        # 群消息
        nick_name = msg["ActualNickName"] if (msg["ActualUserName"] not in my.friends) or \
                                             (not my.friends[msg["ActualUserName"]]["RemarkName"]) else my.friends[msg["ActualUserName"]]["RemarkName"]
    else:
        # 个人消息
        nick_name = wind_name

    we_type = msg["Type"]                       # 消息类型
    we_text = msg["Text"]                       # 消息内容

    return msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_url, wind_name, nick_name, we_type, we_text


# 消息注册，主要处理群消息
@my.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    """
    消息自动接收, 接受全部的消息
    """
    # 消息提取
    msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_url, wind_name, nick_name, we_type, we_text = get_msg_list(msg)

    # 消息过滤, 只监测文字、注解、分享、图片、语音、视频、附件等
    if we_type not in ["Text", "Note", "Sharing", "Picture", "Recording", "Video", "Attachment"]:
        logging.warning("message ignored")
        return

    # 处理来自自己的消息
    if from_user_name == my.loginInfo["User"]["UserName"]:
        return

    # 消息存储，删除过期消息
    my.msg_store[msg_id] = msg
    for _id in [_id for _id in my.msg_store if time.time() - my.msg_store[_id]["CreateTime"] > 120]:
        logging.warning("delete message, message_id = %s", _id)
        my.msg_store.pop(_id)

    # 处理群消息
    if from_user_name.startswith("@@"):
        # 红包消息处理
        if we_type == "Note" and we_text.find("收到红包，请在手机上查看") >= 0:
            my.send("【%s】中有红包，快抢！" % wind_name, toUserName=my.to_user_name)

        # 提到自己消息处理
        if msg["IsAt"]:
            my.send("【%s】中有@你的消息:\nFrom: %s\nTime: %s\n%s" % (wind_name, nick_name, msg_time, msg_content), toUserName=my.to_user_name)

        for key in my.global_keys:
            if msg_content.find(key) >= 0:
                my.send("【%s】中有关键字【%s】:\nFrom: %s\nTime: %s\n%s" % (wind_name, key, nick_name, msg_time, msg_content), toUserName=my.to_user_name)
                break

    # 撤回消息处理
    if we_type == "Note" and we_text.find("撤回了一条消息") >= 0:
        old_msg = my.msg_store.get(msg_content[msg_content.find("<msgid>")+7: msg_content.find("</msgid>")])
        if not old_msg:
            return

        msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_url, wind_name, nick_name, we_type, we_text = get_msg_list(old_msg)
        if we_type in ["Picture", "Recording", "Video", "Attachment"]:
            re_length = re.search("[\"\s]length=\"(?P<length>[\d]+?)\"", msg_content, flags=re.IGNORECASE)
            if (not msg_content) or (re_length and (int(re_length.group("length")) < 5000000)):
                we_text(".Cache/" + msg_file)
                logging.warning("downloading %s to .Cache/", msg_file)
            # 更改内容
            msg_content = msg_file
        elif we_type == "Sharing":
            msg_content = we_text + ": " + msg_url

        my.send("【%s】中有消息被撤回:\nFrom: %s\nType: %s\nTime: %s\n%s" % (wind_name, nick_name, we_type, msg_time, msg_content), toUserName=my.to_user_name)
    return


# 运行程序
my.run()
