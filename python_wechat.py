# _*_ coding: utf-8 _*_

"""
python_wechat.py by xianhu
主要包括如下功能：
(1) 自动提醒群红包
(2) 自动监测被撤回消息
(3) 群统计：发言人数、发言次数等
(4) 群关键字提醒，群被@提醒
"""

import time
import itchat
import logging
import datetime
from itchat.content import *

# 初始化
my = itchat.new_instance()
my.auto_login(hotReload=False, enableCmdQR=-2)
my.global_keys = ["创业", "算法", "人工智能", "机器学习"]
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
    （2）来自群的消息
    （3）来自文件传输助手的消息
    提取消息内容，消息类型分类：
    （1）文字（2）图片（3）语音（4）视频（5）地址（6）名片（7）提醒（8）分享（9）附件
    """
    # logging.warning("message: %s", msg)
    msg_id = msg["MsgId"]                       # 消息ID
    from_user_name = msg["FromUserName"]        # 消息发送者ID，如果为群消息，则为群ID
    to_user_name = msg["ToUserName"]            # 消息接受者ID，如果为群消息，则为群ID

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
    )                                           # 窗口名称：群名或好友名

    msg_user_name = from_user_name              # 消息发送者的ID
    msg_nick_name = wind_name                   # 消息发送者的昵称
    if from_user_name.startswith("@@") or to_user_name.startswith("@@"):
        msg_user_name = msg["ActualUserName"]
        msg_nick_name = msg["ActualNickName"] if (msg_user_name not in my.friends) or (not my.friends[msg_user_name]["RemarkName"]) else my.friends[msg_user_name]["RemarkName"]

    is_at = msg.get("IsAt", None)               # 是否在群内被@
    we_type = msg["Type"]                       # 消息类型
    we_text = msg["Text"]                       # 消息内容

    logging.warning("show: nick_name=%s, wind_name=%s, we_type=%s, we_text=%s, msg_time=%s", msg_nick_name, wind_name, we_type, we_text, msg_time)
    return msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_file_length, msg_voice_length, msg_play_length, msg_url, \
        wind_name, msg_user_name, msg_nick_name, is_at, we_type, we_text


# 消息注册，主要处理群消息
@my.msg_register([TEXT, PICTURE, RECORDING, VIDEO, MAP, CARD, NOTE, SHARING, ATTACHMENT], isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    """
    消息自动接收, 接受全部的消息
    """
    # 消息提取
    msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_file_length, msg_voice_length, msg_play_length, msg_url, \
        wind_name, msg_user_name, msg_nick_name, is_at, we_type, we_text = get_msg_list(msg)

    # 消息过滤, 只监测文字、图片、语音、注解、分享等
    if we_type not in ["Text", "Picture", "Recording", "Note", "Sharing"]:
        logging.warning("message type isn't included, ignored")
        return

    # 处理来自自己的消息
    if from_user_name == my.loginInfo["User"]["UserName"]:
        logging.warning("message is from myself, ignored")
        return

    # 消息存储，删除过期消息
    my.msg_store[msg_id] = msg
    for _id in [_id for _id in my.msg_store if time.time() - my.msg_store[_id]["CreateTime"] > 120]:
        my.msg_store.pop(_id)

    # 保存消息中的内容（图片、语音等），不保存动态图片
    if (we_type in ["Picture", "Recording"]) and (not msg_file.endswith(".gif")):
        try:
            we_text(".Cache/" + msg_file)
            logging.warning("downloading %s to .Cache/", msg_file)
        except Exception as excep:
            logging.error("downloading %s to .Cache/ error: %s", msg_file, excep)

    # ==== 处理红包消息 ====
    if from_user_name.startswith("@@"):
        # ==== 处理红包消息 ====
        if we_type == "Note" and we_text.find("收到红包，请在手机上查看") >= 0:
            my.send("【%s】中【%s】发红包啦，快抢！" % (wind_name, msg_nick_name), toUserName=my.to_user_name)
        # ==== 处理关键词消息 ====
        for key in my.global_keys:
            if we_type == "Text" and we_text.find(key) >= 0:
                my.send("【%s】中【%s】提及关键字：%s" % (wind_name, msg_nick_name, key), toUserName=my.to_user_name)
                my.send(we_text, toUserName=my.to_user_name)
                break
        # ==== 群内是否被@ ====
        if we_type == "Text" and is_at:
            my.send("【%s】中【%s】@了你" % (wind_name, msg_nick_name), toUserName=my.to_user_name)
            my.send(we_text, toUserName=my.to_user_name)

    # ==== 撤回消息处理（必须为最后一步） ====
    if we_type == "Note" and we_text.find("撤回了一条消息") >= 0:
        old_msg = my.msg_store.get(msg_content[msg_content.find("<msgid>")+7: msg_content.find("</msgid>")])
        if not old_msg:
            logging.warning("not message id in my.msg_store")
            return

        msg_id, from_user_name, to_user_name, msg_type, msg_content, msg_time, msg_file, msg_file_length, msg_voice_length, msg_play_length, msg_url, \
            wind_name, msg_user_name, msg_nick_name, is_at, we_type, we_text = get_msg_list(old_msg)
        my.send("【%s】中【%s】撤回了自己发送的消息:\nType: %s\nTime: %s\n%s" % (wind_name, msg_nick_name, we_type, msg_time, msg_file), toUserName=my.to_user_name)

        if we_type == "Text":
            my.send(we_text, toUserName=my.to_user_name)
        elif we_type == "Sharing":
            my.send(we_text + "\n" + msg_url, toUserName=my.to_user_name)
        elif (we_type in ["Picture", "Recording"]) and (not msg_file.endswith(".gif")):
            my.send_image(".Cache/" + msg_file, toUserName=my.to_user_name)

    return


# 运行程序
my.run(debug=False)

"""
好友消息：
{
    'MsgId': '5254859004542036569',
    'FromUserName': '@f3b7fdc54717ea8dc22cb3edef59688e82ef34874e3236801537b94f6cd73e1e',
    'ToUserName': '@e79dde912b8f817514c01f399ca9ba12',
    'MsgType': 1,
    'Content': '[微笑]己改',
    'Status': 3,
    'ImgStatus': 1,
    'CreateTime': 1498448860,
    'VoiceLength': 0,
    'PlayLength': 0,
    'FileName': '',
    'FileSize': '',
    'MediaId': '',
    'Url': '',
    'AppMsgType': 0,
    'StatusNotifyCode': 0,
    'StatusNotifyUserName': '',
    'HasProductId': 0,
    'Ticket': '',
    'ImgHeight': 0,
    'ImgWidth': 0,
    'SubMsgType': 0,
    'NewMsgId': 5254859004542036569,
    'OriContent': '',
    'User': <User: {
        'MemberList': <ContactList: []>,
        'Uin': 0,
        'UserName': '@f3b7fdc54717ea8dc22cb3edef59688e82ef34874e3236801537b94f6cd73e1e',
        'NickName': '付贵吉祥',
        'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgeticon?seq=688475226&username=@f3b7fdc54717ea8dc22cb3edef59688e82ef34874e3236801537b94f6cd73e1e&skey=@',
        'ContactFlag': 3,
        'MemberCount': 0,
        'RemarkName': '付贵吉祥@中建5号楼',
        'HideInputBarFlag': 0,
        'Sex': 1,
        'Signature': '漫漫人生路...',
        'VerifyFlag': 0,
        'OwnerUin': 0,
        'PYInitial': 'FGJX',
        'PYQuanPin': 'fuguijixiang',
        'RemarkPYInitial': 'FGJXZJ5HL',
        'RemarkPYQuanPin': 'fuguijixiangzhongjian5haolou',
        'StarFriend': 0,
        'AppAccountFlag': 0,
        'Statues': 0,
        'AttrStatus': 135205,
        'Province': '山东',
        'City': '',
        'Alias': '',
        'SnsFlag': 17,
        'UniFriend': 0,
        'DisplayName': '',
        'ChatRoomId': 0,
        'KeyWord': '',
        'EncryChatRoomId': '',
        'IsOwner': 0
    }>,
    'Type': 'Text',
    'Text': '[微笑]己改'
}
"""

"""
群消息（来自别人）：
{
    'MsgId': '7844877618948840992',
    'FromUserName': '@@8dc5df044444d1fb8e3972e755b47adf9d07f5a032cae90a4d822b74ee1e4880',
    'ToUserName': '@e79dde912b8f817514c01f399ca9ba12',
    'MsgType': 1,
    'Content': '就是那个，那个协议我们手上有吗',
    'Status': 3,
    'ImgStatus': 1,
    'CreateTime': 1498448972,
    'VoiceLength': 0,
    'PlayLength': 0,
    'FileName': '',
    'FileSize': '',
    'MediaId': '',
    'Url': '',
    'AppMsgType': 0,
    'StatusNotifyCode': 0,
    'StatusNotifyUserName': '',
    'HasProductId': 0,
    'Ticket': '',
    'ImgHeight': 0,
    'ImgWidth': 0,
    'SubMsgType': 0,
    'NewMsgId': 7844877618948840992,
    'OriContent': '',
    'ActualNickName': '5-1-1003',
    'IsAt': False,
    'ActualUserName': '@a0922f18795e4c3b6d7d09c492ace233',
    'User': <Chatroom: {
        'MemberList': <ContactList: [
            <ChatroomMember: {
                'MemberList': <ContactList: []>,
                'Uin': 0,
                'UserName': '@e79dde912b8f817514c01f399ca9ba12',
                'NickName': '齐现虎',
                'AttrStatus': 2147600869,
                'PYInitial': '',
                'PYQuanPin': '',
                'RemarkPYInitial': '',
                'RemarkPYQuanPin': '',
                'MemberStatus': 0,
                'DisplayName': '5-1-1601',
                'KeyWord': 'qix'
            }>,
            <ChatroomMember: {
                'MemberList': <ContactList: []>,
                'Uin': 0,
                'UserName': '@a9620e3d4b82eab2521ccdbb985afc37',
                'NickName': 'A高佳祥15069179911',
                'AttrStatus': 102503,
                'PYInitial': '',
                'PYQuanPin': '',
                'RemarkPYInitial': '',
                'RemarkPYQuanPin': '',
                'MemberStatus': 0,
                'DisplayName': '5-2-220315069179911',
                'KeyWord': 'gao'
            }>,
            .......
        ]>,
        'Uin': 0,
        'UserName': '@@8dc5df044444d1fb8e3972e755b47adf9d07f5a032cae90a4d822b74ee1e4880',
        'NickName': '中建锦绣澜庭二期5#楼',
        'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=0&username=@@8dc5df044444d1fb8e3972e755b47adf9d07f5a032cae90a4d822b74ee1e4880&skey=@',
        'ContactFlag': 3,
        'MemberCount': 106,
        'RemarkName': '',
        'HideInputBarFlag': 0,
        'Sex': 0,
        'Signature': '',
        'VerifyFlag': 0,
        'OwnerUin': 0,
        'PYInitial': 'ZJJXLTEJ5L',
        'PYQuanPin': 'zhongjianjinxiulantingerji5lou',
        'RemarkPYInitial': '',
        'RemarkPYQuanPin': '',
        'StarFriend': 0,
        'AppAccountFlag': 0,
        'Statues': 0,
        'AttrStatus': 0,
        'Province': '',
        'City': '',
        'Alias': '',
        'SnsFlag': 0,
        'UniFriend': 0,
        'DisplayName': '',
        'ChatRoomId': 0,
        'KeyWord': '',
        'EncryChatRoomId': '@d1e510bc8cbd192468e9c85c6f5a9d81',
        'IsOwner': 1,
        'IsAdmin': None,
        'Self': <ChatroomMember: {
            'MemberList': <ContactList: []>,
            'Uin': 0,
            'UserName': '@e79dde912b8f817514c01f399ca9ba12',
            'NickName': '齐现虎',
            'AttrStatus': 2147600869,
            'PYInitial': '',
            'PYQuanPin': '',
            'RemarkPYInitial': '',
            'RemarkPYQuanPin': '',
            'MemberStatus': 0,
            'DisplayName': '5-1-1601',
            'KeyWord': 'qix'
        }>,
        'HeadImgUpdateFlag': 1,
        'ContactType': 0,
        'ChatRoomOwner': '@e79dde912b8f817514c01f399ca9ba12'
    }>,
    'Type': 'Text',
    'Text': '就是那个，那个协议我们手上有吗'
}

群消息（来自自己）：
WARNING: root: message: {
    'MsgId': '6658361167561279652',
    'FromUserName': '@e79dde912b8f817514c01f399ca9ba12',
    'ToUserName': '@@cbd264b76a28d4f5bad27197de60735bc082c95ab49891cf64d745ff4be17e30',
    'MsgType': 1,
    'Content': '看来最近是没有线下活动了',
    'Status': 3,
    'ImgStatus': 1,
    'CreateTime': 1498455090,
    'VoiceLength': 0,
    'PlayLength': 0,
    'FileName': '',
    'FileSize': '',
    'MediaId': '',
    'Url': '',
    'AppMsgType': 0,
    'StatusNotifyCode': 0,
    'StatusNotifyUserName': '',
    'HasProductId': 0,
    'Ticket': '',
    'ImgHeight': 0,
    'ImgWidth': 0,
    'SubMsgType': 0,
    'NewMsgId': 6658361167561279652,
    'OriContent': '',
    'ActualNickName': '齐现虎',
    'IsAt': False,
    'ActualUserName': '@e79dde912b8f817514c01f399ca9ba12',
    'User': <Chatroom: {
        'MemberList': <ContactList: [
            <ChatroomMember: {
                'MemberList': <ContactList: []>,
                'Uin': 0,
                'UserName': '@143b0d468a5be892768e372aae5d3c97f20dd73c6f28a99092fb96d4fc7862e3',
                'NickName': '李小盛',
                'AttrStatus': 235557,
                'PYInitial': '',
                'PYQuanPin': '',
                'RemarkPYInitial': '',
                'RemarkPYQuanPin': '',
                'MemberStatus': 0,
                'DisplayName': '',
                'KeyWord': ''
            }>,
            <ChatroomMember: {
                'MemberList': <ContactList: []>,
                'Uin': 0,
                'UserName': '@edb9eb66b235ef72237ad025290813159b6d3e9cdaa15284ad7f6748b38c2c1f',
                'NickName': '小z@德研社',
                'AttrStatus': 103461,
                'PYInitial': '',
                'PYQuanPin': '',
                'RemarkPYInitial': '',
                'RemarkPYQuanPin': '',
                'MemberStatus': 0,
                'DisplayName': '小z研值512',
                'KeyWord': ''
            }>,
        ]>,
        'Uin': 0,
        'UserName': '@@cbd264b76a28d4f5bad27197de60735bc082c95ab49891cf64d745ff4be17e30',
        'NickName': '德研社z战队',
        'HeadImgUrl': '/cgi-bin/mmwebwx-bin/webwxgetheadimg?seq=688463282&username=@@cbd264b76a28d4f5bad27197de60735bc082c95ab49891cf64d745ff4be17e30&skey=',
        'ContactFlag': 2,
        'MemberCount': 70,
        'RemarkName': '',
        'HideInputBarFlag': 0,
        'Sex': 0,
        'Signature': '',
        'VerifyFlag': 0,
        'OwnerUin': 0,
        'PYInitial': 'DYSZZD',
        'PYQuanPin': 'deyanshezzhandui',
        'RemarkPYInitial': '',
        'RemarkPYQuanPin': '',
        'StarFriend': 0,
        'AppAccountFlag': 0,
        'Statues': 0,
        'AttrStatus': 0,
        'Province': '',
        'City': '',
        'Alias': '',
        'SnsFlag': 0,
        'UniFriend': 0,
        'DisplayName': '',
        'ChatRoomId': 0,
        'KeyWord': '',
        'EncryChatRoomId': '@be08ab93d4d5440069d6617df937b689',
        'IsOwner': 0,
        'IsAdmin': None,
        'Self': <ChatroomMember: {
            'MemberList': <ContactList: []>,
            'Uin': 0,
            'UserName': '@e79dde912b8f817514c01f399ca9ba12',
            'NickName': '齐现虎',
            'AttrStatus': 2147600869,
            'PYInitial': '',
            'PYQuanPin': '',
            'RemarkPYInitial': '',
            'RemarkPYQuanPin': '',
            'MemberStatus': 0,
            'DisplayName': '',
            'KeyWord': 'qix'
        }>
    }>,
    'Type': 'Text',
    'Text': '看来最近是没有线下活动了'
}
"""
