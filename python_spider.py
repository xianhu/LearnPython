# _*_ coding: utf-8 _*_

"""
python_spider.py by xianhu
"""

import urllib.error
import urllib.parse
import urllib.request
import http.cookiejar


# 最简单的方式
response = urllib.request.urlopen("http://www.baidu.com", timeout=10)
html = response.read().decode("utf-8")


# 使用Request类
request = urllib.request.Request("http://www.baidu.com/")
response = urllib.request.urlopen(request, timeout=10)


# 发送数据，即在urlopen()或者Request()中添加data参数
url = "http://localhost/login.php"
data = urllib.parse.urlencode({"act": "login", "email": "xianhu@qq.com", "password": "123456"})
request1 = urllib.request.Request(url, data)			# POST方法
request2 = urllib.request.Request(url + "?%s" % data)   # GET方法
response = urllib.request.urlopen(request, timeout=10)


# 发送Header，即在urlopen()或者Request()中添加headers参数
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)"}
request = urllib.request.Request(url, data=data, headers=headers)   # 参数中添加header参数
request.add_header("Referer", "http://www.baidu.com")		        # add_header函数，另一种添加header的方法
response = urllib.request.urlopen(request, timeout=10)


# 对付"反盗链"：所谓的反盗链设置，就是检查header里的referer站点是不是他自己。所以只需要像把headers的referer改成某个网站自己即可
headers = {"Referer": "http://www.baidu.com/"}


# 引发异常：urllib.error.HTTPError, urllib.error.URLError, 两者存在继承关系
try:
    urllib.request.urlopen(request, timeout=10)
except urllib.error.HTTPError as e:
    print(e.code, e.reason)


# 使用代理，以防止IP被封或IP次数受限：
proxy = urllib.request.ProxyHandler({"http": "111.123.76.12:8080"})

opener = urllib.request.build_opener(proxy)				# 利用代理创建opener实例（OpenerDirector实例）
response = opener.open("https://www.baidu.com/")		# 直接利用opener实例打开url

urllib.request.install_opener(opener)					# 安装、设置全局的opener，然后利用urlopen打开url
response = urllib.request.urlopen("https://www.baidu.com/")


# 抓取网页中的图片：同样适用于抓取网络上的文件。右击鼠标，找到图片属性中的地址，然后进行保存。
url = "http://ww3.sinaimg.cn/large/7d742c99tw1ee7dac2766j204q04qmxq.jpg"
response = urllib.request.urlopen(url, timeout=120)
with open("test.jpg", "wb") as file_img:
    file_img.write(response.read())


# 使用cookie和cookiejar
cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar=cookie_jar))
response = opener.open("https://www.baidu.com/")
for cookie in cookie_jar:
    print(cookie)


# 发送在浏览器中获取的cookie,两种方式:(1)直接放到headers里,(2)构建cookie,添加到cookiejar中
headers = {"User-Agent": "Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)",
           "Cookie": "PHPSESSID=btqkg9amjrtoeev8coq0m78396; USERINFO=n6nxTHTY%2BJA39z6CpNB4eKN8f0KsYLjAQTwPe%2BhLHLruEbjaeh4ulhWAS5RysUM%2B; "}
request = urllib.request.Request(url, headers=headers)

cookie = http.cookiejar.Cookie(name="xx", value="xx", domain="xx")
cookie_jar.set_cookie(cookie)
response = opener.open("https://www.baidu.com/")


# 同时使用代理和cookiejar
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar=cookie_jar))
opener.add_handler(urllib.request.ProxyHandler(proxies={"http": "http://www.example.com:8888/"}))
response = opener.open("https://www.baidu.com/")
