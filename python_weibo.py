# _*_ coding: utf-8 _*_

import re
import rsa
import ssl
import time
import json
import base64
import logging
import binascii
import urllib.parse

# 参考PSpider项目
import spider
ssl._create_default_https_context = ssl._create_unverified_context


class WeiBoLogin(object):
    """
    class of WeiBoLogin, to login weibo.com
    """

    def __init__(self):
        """
        constructor
        """
        self.user_name = None       # 登录用户名
        self.pass_word = None       # 登录密码
        self.user_uniqueid = None   # 用户唯一ID
        self.user_nick = None       # 用户昵称

        self.cookie_jar, self.opener = None, None
        return

    def login(self, user_name, pass_word, proxies=None):
        """
        login weibo.com, return True or False
        """
        # 变量赋值初始化
        self.user_name = user_name
        self.pass_word = pass_word
        self.user_uniqueid = None
        self.user_nick = None

        # 构建cookie_jar和opener,这里不使用代理,同时保证整个流程中不需要关心cookie问题
        self.cookie_jar, self.opener = spider.make_cookiejar_opener(is_cookie=True, proxies=proxies)
        self.opener.addheaders = spider.make_headers(
            user_agent="pc",
            host="weibo.com",
            referer="http://weibo.com/",
            accept="text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            accept_encoding="gzip, deflate",
            accept_language="zh-CN,zh;q=0.8"
        ).items()

        # (1) 打开weibo.com/login.php,先请求一些必要的cookie信息
        self.opener.open("http://weibo.com/login.php")

        # (2) 根据用户名获取加密后的用户名
        s_user_name = self.get_username()

        # (3) 利用加密后的用户名,获取其他一些数据:json格式
        json_data = self.get_json_data(su_value=s_user_name)
        if not json_data:
            return False

        # (4) 根据第三步得到的json数据,获取加密后的密码
        s_pass_word = self.get_password(json_data["servertime"], json_data["nonce"], json_data["pubkey"])

        # (5) 构造登录中用到的postdata
        post_dict = {
            "entry": "weibo",
            "gateway": "1",
            "from": "",
            "savestate": "7",
            "userticket": "1",
            "vsnf": "1",
            "service": "miniblog",
            "encoding": "UTF-8",
            "pwencode": "rsa2",
            "sr": "1280*800",
            "prelt": "529",
            "url": "http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack",
            "rsakv": json_data["rsakv"],
            "servertime": json_data["servertime"],
            "nonce": json_data["nonce"],
            "su": s_user_name,
            "sp": s_pass_word,
            "returntype": "TEXT",
        }

        # (6) 判断是否需要输入验证码,如果需要,获取验证码并进行打码操作
        if json_data.get("showpin", None) == 1:
            url = "http://login.sina.com.cn/cgi/pin.php?r=%d&s=0&p=%s" % (int(time.time()), json_data["pcid"])
            with open("captcha.jpeg", "wb") as file_out:
                file_out.write(self.opener.open(url).read())
            code = input("请输入验证码:")
            # cid, code = self.yundama.get_captcha(self.opener.open(url).read(), "captcha.jpeg", "image/jpeg", codetype="1005")
            # if not code:
            #     return False
            post_dict["pcid"] = json_data["pcid"]
            post_dict["door"] = code

        # (7) 根据构造的postdata,登录微博
        login_url_1 = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.18)&_=%d" % int(time.time())
        json_data_1 = json.loads(spider.get_html_content(self.opener.open(login_url_1, data=spider.make_post_data(post_dict))))
        if json_data_1["retcode"] == "0":
            # 登录后有一个跳转, 构造跳转链接的postdata
            post_dict = {
                "callback": "sinaSSOController.callbackLoginStatus",
                "ticket": json_data_1["ticket"],
                "ssosavestate": int(time.time()),
                "client": "ssologin.js(v1.4.18)",
                "_": int(time.time()*1000),
            }
            login_url_2 = "https://passport.weibo.com/wbsso/login?" + urllib.parse.urlencode(post_dict)
            html_data = spider.get_html_content(self.opener.open(login_url_2), charset="gbk")
            json_data_2 = json.loads(re.search("\((?P<result>.*)\)", html_data).group("result"))

            # 检查登录是否成功,并获取用户唯一ID,用户昵称等
            if json_data_2["result"] is True:
                self.user_uniqueid = json_data_2["userinfo"]["uniqueid"]
                self.user_nick = json_data_2["userinfo"]["displayname"]
                logging.warning("WeiBoLogin succeed: %s", json_data_2)
            else:
                logging.warning("WeiBoLogin failed: %s", json_data_2)
        else:
            logging.warning("WeiBoLogin failed: %s", json_data_1)
        return True if self.user_uniqueid and self.user_nick else False

    def get_username(self):
        """
        get username, encrypt file: http://tjs.sjs.sinajs.cn/t5/register/js/page/remote/loginLayer.js
        """
        username_quote = urllib.parse.quote_plus(self.user_name)
        username_base64 = base64.b64encode(username_quote.encode("utf-8"))
        return username_base64.decode("utf-8")

    def get_json_data(self, su_value):
        """
        get the value of "servertime", "nonce", "pubkey", "rsakv" and "showpin", etc
        """
        post_data = urllib.parse.urlencode({
            "entry": "weibo",
            "callback": "sinaSSOController.preloginCallBack",
            "rsakt": "mod",
            "checkpin": "1",
            "client": "ssologin.js(v1.4.18)",
            "su": su_value,
            "_": int(time.time()*1000),
        })

        try:
            response = self.opener.open('http://login.sina.com.cn/sso/prelogin.php?'+post_data)
            data = spider.get_html_content(response, charset="utf-8")
            json_data = json.loads(re.search("\((?P<data>.*)\)", data).group("data"))
        except Exception as excep:
            json_data = {}
            logging.error("WeiBoLogin get_json_data error: %s", excep)

        logging.debug("WeiBoLogin get_json_data: %s", json_data)
        return json_data

    def get_password(self, servertime, nonce, pubkey):
        """
        get legal password, encrypt file: http://tjs.sjs.sinajs.cn/t5/register/js/page/remote/loginLayer.js
        """
        string = (str(servertime) + '\t' + str(nonce) + '\n' + str(self.pass_word)).encode("utf-8")
        public_key = rsa.PublicKey(int(pubkey, 16), int("10001", 16))
        password = rsa.encrypt(string, public_key)
        password = binascii.b2a_hex(password)
        return password.decode()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(asctime)s\t%(levelname)s\t%(message)s")
    # 测试登录,输入微博的用户名和密码
    weibo = WeiBoLogin()
    weibo.login("username", "password")
