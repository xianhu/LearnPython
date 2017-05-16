# _*_ coding: utf-8 _*_

"""
python_wechat.py by xianhu
主要包括如下功能：
(1) 自动提醒群红包
(2) 自动保存被撤回消息，包括内容、文件、图片、语音、视频等
"""

import time
import itchat
import logging
import datetime
from itchat.content import *

# 初始化
my = itchat.new_instance()
my.auto_login(hotReload=False, enableCmdQR=2)
my.global_keys = ["创业", "算法", "人工智能"]
my.to_user_name = "filehelper"

# my还包括的以下属性，注意用点.查看：
# (1) alive 是否还活着，isLogging 是否已登陆
# (2) loginInfo 登陆信息，其中的User属性为自己的信息User字典类，包括UserName, NickName, RemarkName, Sex(1 or 2), Signature, Province, City等
# (3) memberList 通讯录列表，每一项为一个User字典类，包括UserName, NickName, RemarkName, Sex(1 or 2), Signature, Province, City等
# (4) chatroomList 群聊列表，每一项为一个Chatroom字典类，包括UserName, NickName, RemarkName, MemberCount, MemberList, Self等
# (5) mpList 订阅号列表，每一项为一个MassivePlatform字典类，包括UserName, NickName等

# 获取并更新通讯录: {UserName: UserInstance}
my.friends = {user["UserName"]: user for user in my.get_friends(update=True)}

# 消息存储队列
my.msg_store = {}


# 消息提取函数
def get_msg_list(msg):
    """
    提取消息内容，消息来源分类：
    （1）来自好友的消息
    （2）来自自己的消息
    （3）来自文件传输助手的消息
    （4）来自群聊的消息
    提取消息内容，消息类型分类：
    （1）文字
    （2）图片
    （3）语音
    （4）视频
    （5）地址
    （6）名片
    （7）Note
    （8）分享
    （9）附件
    """
    logging.warning("message: %s", msg)
    msg_id = msg["MsgId"]                       # 消息ID
    from_user_name = msg["FromUserName"]        # 消息发送者ID
    to_user_name = msg["ToUserName"]            # 消息接受者ID

    msg_type = msg["MsgType"]                   # 消息类型
    msg_content = msg["Content"]                # 消息内容
    msg_time = datetime.datetime.fromtimestamp(msg["CreateTime"])  # 消息发送时间

    msg_file = msg["FileName"]                  # 消息中所带文件的名称
    msg_file_length = msg["FileSize"]           # 消息中所带文件的大小
    msg_file_length = int(msg_file_length) if msg_file_length.strip() else 0
    msg_voice_length = msg["VoiceLength"]       # 消息中所带语音的长度（毫秒）
    msg_play_length = msg["PlayLength"]         # 消息中所带视频的长度（秒）
    msg_url = msg["Url"]                        # 消息中所带链接的地址

    wind_name = msg["User"]["RemarkName"] if msg["User"].get("RemarkName") else (
        msg["User"]["NickName"] if msg["User"].get("NickName") else to_user_name
    )

    if from_user_name.startswith("@@"):
        nick_name = msg["ActualNickName"] if (msg["ActualUserName"] not in my.friends) or \
                                             (not my.friends[msg["ActualUserName"]]["RemarkName"]) else my.friends[msg["ActualUserName"]]["RemarkName"]
    else:
        nick_name = wind_name

    we_type = msg["Type"]                       # 消息类型
    we_text = msg["Text"]                       # 消息内容

    logging.warning("show: nick_name=%s, wind_name=%s, we_type=%s, we_text=%s", nick_name, wind_name, we_type, we_text)
    return msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, \
        msg_file, msg_file_length, msg_voice_length, msg_play_length, msg_url, wind_name, nick_name, we_type, we_text


# 消息注册，主要处理群消息
@my.msg_register([TEXT, MAP, CARD, NOTE, SHARING, PICTURE, RECORDING, ATTACHMENT, VIDEO], isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    """
    消息自动接收, 接受全部的消息
    """
    # 消息提取
    msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, \
        msg_file, msg_file_length, msg_voice_length, msg_play_length, msg_url, wind_name, nick_name, we_type, we_text = get_msg_list(msg)

    # 消息过滤, 只监测文字、注解、分享、图片、语音、视频、附件等
    if we_type not in ["Text", "Note", "Sharing", "Picture", "Recording", "Video", "Attachment"]:
        logging.warning("message type isn't included, ignored")
        return

    # 处理来自自己的消息
    if from_user_name == my.loginInfo["User"]["UserName"]:
        logging.warning("message is from myself, ignored")
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

    # 撤回消息处理
    if we_type == "Note" and we_text.find("撤回了一条消息") >= 0:
        old_msg = my.msg_store.get(msg_content[msg_content.find("<msgid>")+7: msg_content.find("</msgid>")])
        if not old_msg:
            logging.warning("not message id in my.msg_store")
            return

        msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, \
            msg_file, msg_file_length, msg_voice_length, msg_play_length, msg_url, wind_name, nick_name, we_type, we_text = get_msg_list(old_msg)

        if we_type == "Text":
            msg_content = we_text
        elif we_type in ["Picture", "Recording", "Video", "Attachment"]:
            if (msg_file_length <= 500000) and (msg_voice_length <= 60000) and (msg_play_length <= 10):
                try:
                    we_text(".Cache/" + msg_file)
                    logging.warning("downloading %s to .Cache/", msg_file)
                except:
                    logging.error("downloading %s to .Cache/ error", msg_file)
            msg_content = msg_file
        elif we_type == "Sharing":
            msg_content = we_text + ": " + msg_url

        my.send("【%s】中有消息被撤回:\nFrom: %s\nType: %s\nTime: %s\n%s" % (wind_name, nick_name, we_type, msg_time, msg_content), toUserName=my.to_user_name)
    return


# 运行程序
my.run()
