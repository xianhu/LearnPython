# _*_ coding: utf-8 _*_

"""
python_spider.py by xianhu
"""

import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar

# 首先定义下边可能需要的变量
url = "https://www.baidu.com"
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}

# 最简单的网页抓取方式
response = urllib.request.urlopen(url, timeout=10)
html = response.read().decode("utf-8")


# 使用Request实例代替url
request = urllib.request.Request(url, data=None, headers={})
response = urllib.request.urlopen(request, timeout=10)


# 发送数据，即在Request()中添加data参数
data = urllib.parse.urlencode({"act": "login", "email": "xianhu@qq.com", "password": "123456"})
request1 = urllib.request.Request(url, data=data)           # POST方法
request2 = urllib.request.Request(url+"?%s" % data)         # GET方法
response = urllib.request.urlopen(request, timeout=10)


# 发送Header，即在Request()中添加headers参数
request = urllib.request.Request(url, data=data, headers=headers)   # 参数中添加header参数
request.add_header("Referer", "http://www.baidu.com")               # 另一种添加header的方式,添加Referer是为了应对"反盗链"
response = urllib.request.urlopen(request, timeout=10)


# 网页抓取引发异常：urllib.error.HTTPError, urllib.error.URLError, 两者存在继承关系
try:
    urllib.request.urlopen(request, timeout=10)
except urllib.error.HTTPError as e:
    print(e.code, e.reason)
except urllib.error.URLError as e:
    print(e.errno, e.reason)


# 使用代理，以防止IP被封或IP次数受限：
proxy_handler = urllib.request.ProxyHandler(proxies={"http": "111.123.76.12:8080"})

opener = urllib.request.build_opener(proxy_handler)     # 利用代理创建opener实例
response = opener.open(url)                             # 直接利用opener实例打开url

urllib.request.install_opener(opener)                   # 安装全局opener，然后利用urlopen打开url
response = urllib.request.urlopen(url)


# 使用cookie和cookiejar,应对服务器检查
cookie_jar = http.cookiejar.CookieJar()
cookie_jar_handler = urllib.request.HTTPCookieProcessor(cookiejar=cookie_jar)
opener = urllib.request.build_opener(cookie_jar_handler)
response = opener.open(url)


# 发送在浏览器中获取的cookie,两种方式:
# (1)直接放到headers里
headers = {
    "User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
    "Cookie": "PHPSESSID=btqkg9amjrtoeev8coq0m78396; USERINFO=n6nxTHTY%2BJA39z6CpNB4eKN8f0KsYLjAQTwPe%2BhLHLruEbjaeh4ulhWAS5RysUM%2B; "
}
request = urllib.request.Request(url, headers=headers)

# (2)构建cookie,添加到cookiejar中
cookie = http.cookiejar.Cookie(name="xx", value="xx", domain="xx", ...)
cookie_jar.set_cookie(cookie)
response = opener.open(url)


# 同时使用代理和cookiejar
opener = urllib.request.build_opener(cookie_jar_handler)
opener.add_handler(proxy_handler)
response = opener.open("https://www.baidu.com/")


# 抓取网页中的图片：同样适用于抓取网络上的文件。右击鼠标，找到图片属性中的地址，然后进行保存。
response = urllib.request.urlopen("http://ww3.sinaimg.cn/large/7d742c99tw1ee7dac2766j204q04qmxq.jpg", timeout=120)
with open("test.jpg", "wb") as file_img:
    file_img.write(response.read())


# HTTP认证：即HTTP身份验证
password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()     # 创建一个PasswordMgr
password_mgr.add_password(realm=None, uri=url, user='username', passwd='password')   # 添加用户名和密码
handler = urllib.request.HTTPBasicAuthHandler(password_mgr)         # 创建HTTPBasicAuthHandler
opener = urllib.request.build_opener(handler)                       # 创建opner
response = opener.open(url, timeout=10)                             # 获取数据
