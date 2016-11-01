# _*_ coding: utf-8 _*_

"""
python_requests.py by xianhu
"""

import requests

# 尝试获取某个网页, 这里的r是一个Response对象
r = requests.get("https://github.com/timeline.json")
print(type(r))

# Requests简便的API意味着所有HTTP请求类型都是显而易见的
r1 = requests.post("http://httpbin.org/post")
r2 = requests.put("http://httpbin.org/put")
r3 = requests.delete("http://httpbin.org/delete")
r4 = requests.head("http://httpbin.org/get")
r5 = requests.options("http://httpbin.org/get")

# 传递URL参数: 字典
payload = {"key1": "value1", "key2": "value2"}
r = requests.get("http://httpbin.org/get", params=payload)
print(r.url)                # http://httpbin.org/get?key2=value2&key1=value1

# 传递URL参数: 字典里带有列表
payload = {"key1": "value1", "key2": ["value2", "value3"]}
r = requests.get("http://httpbin.org/get", params=payload)
print(r.url)                # http://httpbin.org/get?key1=value1&key2=value2&key2=value3

# 获取正常内容
r = requests.get("https://github.com/timeline.json")
print(r.text)               # "[{"repository":{"open_issues":0,"url":"https://github.com/...
print(r.encoding)           # "utf-8"

# Requests会自动解码来自服务器的内容(基于HTTP头部对响应的编码作出有根据的推测), 或者你自己更改
r.encoding = "ISO-8859-1"
print(r.text)               # 此时使用新的r.encoding新值

# 二进制响应内容, Requests会自动为你解码 gzip 和 deflate 传输编码的响应数据
print(r.content)            # b"[{"repository":{"open_issues":0,"url":"https://github.com/...

# JSON 响应内容, Requests中也有一个内置的JSON解码器
print(r.json())             # [{u"repository": {u"open_issues": 0, u"url": "https://github.com/...

# 原始响应内容: 获取来自服务器的原始套接字响应
r = requests.get("https://github.com/timeline.json", stream=True)
print(r.raw)                # <requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
print(r.raw.read(10))       # "\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03"

# 但一般情况下, 应该以下面的模式将文本流保存到文件
with open("test", "wb") as fd:
    for chunk in r.iter_content(chunk_size=256):
        fd.write(chunk)

# 定制请求头: 一个字典
headers = {"user-agent": "my-app/0.0.1"}
r = requests.get("https://api.github.com/some/endpoint", headers=headers)
print(r.request.headers)    # 获取该请求的头部

# 更加复杂的POST请求: 表单
payload = {"key1": "value1", "key2": "value2"}
r = requests.post("http://httpbin.org/post", data=payload)
print(r.text)

# POST一个多部分编码(Multipart-Encoded)的文件
files = {"file": open("report.xls", "rb")}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)

# 你可以显式地设置文件名, 文件类型和请求头
files = {"file": ("report.xls", open("report.xls", "rb"), "application/vnd.ms-excel", {"Expires": "0"})}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)

# 你也可以发送作为文件来接收的字符串
files = {"file": ("report.csv", "some,data,to,send\nanother,row,to,send\n")}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)

# 响应状态码
r = requests.get("http://httpbin.org/get")
print(r.status_code)                            # 200
print(r.status_code == requests.codes.ok)       # True 响应状态码查询

# 如果发送了一个错误请求(4XX客户端错误, 或5XX服务器错误响应), 可以通过 Response.raise_for_status() 来抛出异常:
bad_r = requests.get("http://httpbin.org/status/404")
print(bad_r.status_code)                        # 404
bad_r.raise_for_status()
# Traceback (most recent call last):
#   File "requests/models.py", line 832, in raise_for_status
#     raise http_error
# requests.exceptions.HTTPError: 404 Client Error

# 响应头, 一个Python字典形式展示的服务器响应头, HTTP头部是大小写不敏感的
print(r.headers)
# {
#     "content-encoding": "gzip",
#     "transfer-encoding": "chunked",
#     "connection": "close",
#     "server": "nginx/1.0.4",
#     "x-runtime": "148ms",
#     "etag": "e1ca502697e5c9317743dc078f67693f",
#     "content-type": "application/json"
# }
print(r.headers["Content-Type"])                # "application/json"
print(r.headers.get("content-type"))            # "application/json"

# Cookie: 如果某个响应中包含一些 cookie
r = requests.get("http://example.com/some/cookie/setting/url")
print(r.cookies["example_cookie_name"])         # "example_cookie_value"

# 要想发送你的cookies到服务器, 可以使用cookies参数, 一个字典
cookies = dict(cookies_are="working")
r = requests.get("http://httpbin.org/cookies", cookies=cookies)
print(r.text)

# 会话对象: 会话对象让你能够跨请求保持某些参数, 它也会在同一个 Session 实例发出的所有请求之间保持cookie
s = requests.Session()
s.get("http://httpbin.org/cookies/set/sessioncookie/123456789")
r = s.get("http://httpbin.org/cookies")
print(r.text)                                   # '{"cookies": {"sessioncookie": "123456789"}}'

# 会话也可用来为请求方法提供缺省数据, 这是通过为会话对象的属性提供数据来实现的
s = requests.Session()
s.auth = ("user", "pass")
s.headers.update({"x-test": "true"})
s.get("http://httpbin.org/headers", headers={"x-test2": "true"})    # both "x-test" and "x-test2" are sent

# 不过需要注意, 就算使用了会话, 方法级别的参数也不会被跨请求保持
# 下面的例子只会和第一个请求发送cookie, 而非第二个
s = requests.Session()
r = s.get("http://httpbin.org/cookies", cookies={"from-my": "browser"})
print(r.text)                                   # '{"cookies": {"from-my": "browser"}}'
r = s.get("http://httpbin.org/cookies")
print(r.text)                                   # '{"cookies": {}}'
# 如果你要手动为会话添加 cookie, 就是用 Cookie utility 函数来操纵Session.cookies

# 会话还可以用作前后文管理器
with requests.Session() as s:
    s.get("http://httpbin.org/cookies/set/sessioncookie/123456789")

# 重定向与请求历史, 默认情况下, 除了HEAD, Requests会自动处理所有重定向
# 可以使用响应对象的history方法来追踪重定向
# Response.history 是一个 Response 对象的列表, 为了完成请求而创建了这些对象. 这个对象列表按照从最老到最近的请求进行排序
r = requests.get("http://github.com")
print(r.status_code)                            # 200
print(r.history)                                # [<Response [301]>]

# 如果你使用的是GET、OPTIONS、POST、PUT、PATCH 或者 DELETE, 那么你可以通过 allow_redirects 参数禁用重定向处理
r = requests.get("http://github.com", allow_redirects=False)
print(r.status_code)                            # 301
print(r.history)                                # []

# 如果你使用了HEAD, 你也可以启用重定向
r = requests.head("http://github.com", allow_redirects=True)
print(r.history)                                # [<Response [301]>]

# 超时, 设置timeout参数
requests.get("http://github.com", timeout=0.001)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# requests.exceptions.Timeout: HTTPConnectionPool(host="github.com", port=80): Request timed out. (timeout=0.001)

# 注意: timeout仅对连接过程有效, 与响应体的下载无关
# timeout并不是整个下载响应的时间限制, 而是如果服务器在timeout秒内没有应答, 将会引发一个异常
# 更精确地说, 是在 timeout 秒内没有从基础套接字上接收到任何字节的数据时
requests.get("https://github.com", timeout=5)
# 这一 timeout 值将会用作 connect 和 read 二者的 timeout
# 如果要分别制定, 就传入一个元组
requests.get("https://github.com", timeout=(3.05, 27))

# 错误与异常: 遇到网络问题(如: DNS 查询失败、拒绝连接等)时, Requests 会抛出一个 ConnectionError 异常
# 如果 HTTP 请求返回了不成功的状态码, Response.raise_for_status() 会抛出一个 HTTPError 异常
# 若请求超时, 则抛出一个 Timeout 异常
# 若请求超过了设定的最大重定向次数, 则会抛出一个 TooManyRedirects 异常
# 所有Requests显式抛出的异常都继承自 requests.exceptions.RequestException

# SSL证书验证, verify设置为True表示检查证书, 设置为False表示忽略证书
requests.get("https://kennethreitz.com", verify=True)       # 未设置SSL证书, 抛出异常
# requests.exceptions.SSLError: hostname "kennethreitz.com" doesn"t match either of "*.herokuapp.com", "herokuapp.com"
requests.get("https://github.com", verify=True)             # <Response [200]>, 已设置SSL证书
# 对于私有证书，你也可以传递一个 CA_BUNDLE 文件的路径给 verify

# 你也可以指定一个本地证书用作客户端证书, 可以是单个文件（包含密钥和证书）或一个包含两个文件路径的元组:
requests.get("https://kennethreitz.com", cert=("/path/server.crt", "/path/key"))
requests.get("https://kennethreitz.com", cert="/wrong_path/server.pem")
# SSLError: [Errno 336265225] _ssl.c:347: error:140B0009:SSL routines:SSL_CTX_use_PrivateKey_file:PEM lib
# 警告: 本地证书的私有 key 必须是解密状态. 目前Requests不支持使用加密的 key

# 流式上传, 允许你发送大的数据流或文件而无需先把它们读入内存
with open("massive-body") as f:
    requests.post("http://some.url/streamed", data=f)


# 事件挂钩, 可用的钩子: response(从一个请求产生的响应)
# 你可以通过传递一个 {hook_name: callback_function} 字典给 hooks 请求参数为每个请求分配一个钩子函数
def print_url(resp):
    print(resp.url)
    return
requests.get("http://httpbin.org", hooks=dict(response=print_url))

# 代理
proxies = {
    "http": "http://10.10.1.10:3128",
    "https": "http://10.10.1.10:1080",
}
requests.get("http://example.org", proxies=proxies)
# 若代理需要使用HTTP Basic Auth, 可以使用http://user:password@host:port/, 比如"http": "http://user:pass@10.10.1.10:3128/"

# 除了基本的 HTTP 代理, Request 还支持 SOCKS 协议的代理
# $ pip install requests[socks]
proxies = {
    "http": "socks5://user:pass@host:port",
    "https": "socks5://user:pass@host:port"
}
requests.get("http://example.org", proxies=proxies)
