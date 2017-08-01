# _*_ coding: utf-8 _*_

"""
python_wechat.py by xianhu
主要包括如下功能：
(1) 自动提醒群红包
(2) 自动监测被撤回消息
(3) 群关键字提醒，群被@提醒
"""

import time
import itchat
import logging
from itchat.content import *

# 初始化
my = itchat.new_instance()
my.auto_login(hotReload=False, enableCmdQR=2)

# my还包括的以下属性，注意用点.查看：
# (1) alive 是否还活着，isLogging 是否已登陆
# (2) loginInfo 登陆信息，其中的User属性为自己的信息User字典类，包括UserName, NickName, RemarkName, Sex(1 or 2), Signature, Province, City等
# (3) memberList 通讯录列表，每一项为一个User字典类，包括UserName, NickName, RemarkName, Sex(1 or 2), Signature, Province, City等
# (4) chatroomList 群聊列表，每一项为一个Chatroom字典类，包括UserName, NickName, RemarkName, MemberCount, MemberList, Self等
# (5) mpList 订阅号列表，每一项为一个MassivePlatform字典类，包括UserName, NickName等

my.global_keys = ["创业", "人工智能", "企业服务"]
my.to_user_name = "filehelper"      # 消息接受者
my.update_time = time.time()        # 信息更新时间
my.msg_store = {}                   # 消息存储队列
my.friends = {}                     # 好友字典列表
my.groups = {}                      # 群聊字典列表


def update_my_infos():
    """
    更新信息
    """
    # 获取并更新通讯录: {UserName: UserInstance}
    my.friends = {user["UserName"]: user for user in my.get_friends(update=True)}
    # 获取并更新群列表: {UserName: UserInstance}
    my.groups = {group["UserName"]: group for group in my.get_chatrooms(update=True)}
    return
update_my_infos()


class Message(object):
    """
    消息类
    """
    def __init__(self, msg):
        """
        构造函数：提取消息内容
        消息来源分类：
        （1）来自好友的消息
        （2）来自群的消息
        提取消息内容，消息类型分类：
        （1）文字（2）图片（3）语音（4）视频（5）地址（6）名片（7）提醒（8）分享（9）附件
        """
        # 更新信息，十分钟更新一次
        # logging.warning("message: %s", msg)
        if time.time() - my.update_time > 600:
            update_my_infos()
            my.update_time = time.time()

        self.msg_id = msg["MsgId"]                      # 消息ID
        self.from_user_name = msg["FromUserName"]       # 消息发送者ID，如果为群消息，则为群ID

        self.msg_type = msg["MsgType"]                  # 消息类型，这里参考下边的we_type
        self.msg_content = msg["Content"]               # 消息内容，这里参考下边的we_text
        self.msg_time = msg["CreateTime"]               # 消息发送时间，时间戳格式

        self.msg_file = msg["FileName"]                 # 消息中所带文件的名称
        self.msg_file_length = msg["FileSize"]          # 消息中所带文件的大小，字符串类型
        self.msg_voice_length = msg["VoiceLength"]      # 消息中所带语音的长度（毫秒）
        self.msg_play_length = msg["PlayLength"]        # 消息中所带视频的长度（秒）
        self.msg_url = msg["Url"]                       # 消息中所带链接的地址

        self.user_user_name = msg["User"].get("UserName", "")       # 消息发送者ID，如果为群消息，则为群ID
        self.user_nick_name = msg["User"].get("NickName", "")       # 消息发送者昵称，如果为群消息，则为群名
        self.user_remark_name = msg["User"].get("RemarkName", "")   # 消息发送者备注名称，如果为群消息，则为群备注名称
        self.wind_name = self.user_remark_name if self.user_remark_name else (
            self.user_nick_name if self.user_nick_name else (
                my.friends[self.user_user_name]["NickName"] if self.user_user_name in my.friends else (
                    my.groups[self.user_user_name]["NickName"] if self.user_user_name in my.groups else "未知窗口"
                )
            )
        )

        self.actual_user_name = msg.get("ActualUserName", "")       # 群消息中，消息发送者的ID
        self.actual_nick_name = msg.get("ActualNickName", "")       # 群消息中，消息发送者的群昵称
        self.actual_remark_name = self.actual_nick_name \
            if (self.actual_user_name not in my.friends) or (not my.friends[self.actual_user_name]["RemarkName"]) \
            else my.friends[self.actual_user_name]["RemarkName"]

        self.is_at = msg.get("IsAt", None)              # 是否在群内被@
        self.we_type = msg["Type"]                      # 消息类型
        self.we_text = msg["Text"]                      # 消息内容

        logging.warning("wind_name=%s, send_name=%s, we_type=%s, we_text=%s", self.wind_name, self.actual_remark_name, self.we_type, self.we_text)
        return


def process_message_group(msg):
    """
    处理群消息
    """
    # ==== 处理红包消息 ====
    if msg.we_type == "Note" and msg.we_text.find("收到红包，请在手机上查看") >= 0:
        my.send("【%s】中有人发红包啦，快抢！" % msg.wind_name, toUserName=my.to_user_name)

    # ==== 处理关键词消息 ====
    for key in my.global_keys:
        if msg.we_type == "Text" and msg.we_text.find(key) >= 0:
            my.send("【%s】中【%s】提及了关键字：%s" % (msg.wind_name, msg.actual_remark_name, key), toUserName=my.to_user_name)
            my.send(msg.we_text, toUserName=my.to_user_name)
            break

    # ==== 群内是否被@ ====
    if msg.we_type == "Text" and msg.is_at:
        my.send("【%s】中【%s】@了你" % (msg.wind_name, msg.actual_remark_name), toUserName=my.to_user_name)
        my.send(msg.we_text, toUserName=my.to_user_name)
    return


def process_message_revoke(msg):
    """
    处理撤回消息
    """
    # 消息存储，删除过期消息
    my.msg_store[msg.msg_id] = msg
    for _id in [_id for _id in my.msg_store if time.time() - my.msg_store[_id].msg_time > 120]:
        my.msg_store.pop(_id)

    # 保存消息中的内容（图片、语音等）
    if msg.we_type in ["Picture", "Recording"]:
        try:
            msg.we_text(".Cache/" + msg.msg_file)
            logging.warning("process_message_revoke: download %s to .Cache/", msg.msg_file)
        except Exception as excep:
            logging.error("process_message_revoke: download %s to .Cache/ error: %s", msg.msg_file, excep)

    # ==== 撤回消息处理（必须为最后一步） ====
    if msg.we_type == "Note" and msg.we_text.find("撤回了一条消息") >= 0:
        old_msg = my.msg_store.get(msg.msg_content[msg.msg_content.find("<msgid>")+7: msg.msg_content.find("</msgid>")])
        if not old_msg:
            logging.warning("process_message_revoke: no message id in my.msg_store")
            return

        if old_msg.from_user_name.startswith("@@"):
            my.send("【%s】中【%s】撤回了自己发送的消息:\nType: %s\n%s" %
                    (old_msg.wind_name, old_msg.actual_remark_name, old_msg.we_type, old_msg.msg_file), toUserName=my.to_user_name)
        else:
            my.send("【%s】撤回了自己发送的消息:\nType: %s\n%s" %
                    (old_msg.wind_name, old_msg.we_type, old_msg.msg_file), toUserName=my.to_user_name)

        if old_msg.we_type in ["Text", "Card"]:
            my.send(str(old_msg.we_text), toUserName=my.to_user_name)
        elif old_msg.we_type == "Sharing":
            my.send(old_msg.we_text + "\n" + old_msg.msg_url, toUserName=my.to_user_name)
        elif old_msg.we_type == "Picture":
            my.send_image(".Cache/" + old_msg.msg_file, toUserName=my.to_user_name)
        elif old_msg.we_type == "Recording":
            my.send_file(".Cache/" + old_msg.msg_file, toUserName=my.to_user_name)
    return


@my.msg_register([TEXT, PICTURE, RECORDING, VIDEO, MAP, CARD, NOTE, SHARING, ATTACHMENT], isFriendChat=True, isGroupChat=True)
def text_reply(msg):
    """
    消息自动接收, 接受全部的消息（自己发送的消息除外）
    """
    # 跳过来自自己的消息
    if msg["FromUserName"] == my.loginInfo["User"]["UserName"]:
        return

    # 消息提取
    msg = Message(msg)

    # 消息过滤, 只监测文字、图片、语音、名片、注解、分享等
    if msg.we_type not in ["Text", "Picture", "Recording", "Card", "Note", "Sharing"]:
        logging.warning("process_message_group: message type isn't included, ignored")
        return

    # 处理群消息
    if msg.from_user_name.startswith("@@"):
        process_message_group(msg)

    # 处理撤回消息
    process_message_revoke(msg)
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
群消息：
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

警示消息：好友类
{
    'MsgId': '1529895072288746571',
    'FromUserName': '@4076708be2e09ef83f249f168553d0dd55b4f734aee7d276e92ddbe98625476a',
    'ToUserName': '@f97583d8ffbaee6189854116897c677f',
    'MsgType': 10000,
    'Content': '你已添加了呼啸而过的小青春，现在可以开始聊天了。',
    'Status': 4,
    'ImgStatus': 1,
    'CreateTime': 1498533407,
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
    'NewMsgId': 1529895072288746571,
    'OriContent': '',
    'User': <User: {
        'userName': '@4076708be2e09ef83f249f168553d0dd55b4f734aee7d276e92ddbe98625476a',
        'MemberList': <ContactList: []>
    }>,
    'Type': 'Note',
    'Text': '你已添加了呼啸而过的小青春，现在可以开始聊天了。'
}

警示消息：群类
{
    'MsgId': '1049646282086057263',
    'FromUserName': '@@300f57b68ca7ef593ae3221eef7dba5377466c86122aaa15a8ffc1031310e210',
    'ToUserName': '@006f63e8086ab07fcbe3771dc824c4a6',
    'MsgType': 10000,
    'Content': '你邀请"大姐"加入了群聊',
    'Status': 3,
    'ImgStatus': 1,
    'CreateTime': 1498533901,
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
    'NewMsgId': 1049646282086057263,
    'OriContent': '',
    'ActualUserName': '@006f63e8086ab07fcbe3771dc824c4a6',
    'ActualNickName': '某某某',
    'IsAt': False,
    'User': <Chatroom: {
        'UserName': '@@300f57b68ca7ef593ae3221eef7dba5377466c86122aaa15a8ffc1031310e210',
        'MemberList': <ContactList: []>
    }>,
    'Type': 'Note',
    'Text': '你邀请"大姐"加入了群聊'
}
"""
