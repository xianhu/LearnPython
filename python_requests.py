# _*_ coding: utf-8 _*_

"""
python_requests.py by xianhu
"""

import requests.adapters

# 不同方式获取网页内容, 返回一个Response对象, 请求的参数可以为url或Request对象
r0 = requests.get("https://github.com/timeline.json")
r1 = requests.post("http://httpbin.org/post")
r2 = requests.put("http://httpbin.org/put")
r3 = requests.delete("http://httpbin.org/delete")
r4 = requests.head("http://httpbin.org/get")
r5 = requests.options("http://httpbin.org/get")
r6 = requests.patch("http://httpbin.org/get")

# Request对象:
# class requests.Request(method=None, url=None, headers=None, files=None, data=None, params=None, auth=None, cookies=None, hooks=None, json=None)

# 上边所有的获取方式都调用底层的request方法, 所以request方法有的参数, 上边几个函数都应该有:
# requests.request(method, url, **kwargs)
# kwargs包括: params / data / json / headers / cookies / files / auth / timeout / allow_redirects(bool) / proxies / verify(bool) / stream / cert

# Response对象: class requests.Response
# 包含的主要属性: content / cookies / encoding / headers / history / is_permanent_redirect / is_redirect / reason / status_code / text / url 等
# 包含的主要方法: iter_content(chunk_size=1, decode_unicode=False) / iter_lines(chunk_size=512, decode_unicode=None, delimiter=None)
# 包含的主要方法: close() / json(**kwargs) / raise_for_status() 等

# 以字典的形式传递URL参数, 也可以直接以?xx=xx&xx=xx的形式将其放在url后
params = {"key1": "value1", "key2": "value2"}
r = requests.get("http://httpbin.org/get", params=params)
print(r.url)                # http://httpbin.org/get?key2=value2&key1=value1

# 以字典的形式传递URL参数: 字典里带有列表
params = {"key1": "value1", "key2": ["value2", "value3"]}
r = requests.get("http://httpbin.org/get", params=params)
print(r.url)                # http://httpbin.org/get?key1=value1&key2=value2&key2=value3

# 获取网页内容
r = requests.get("https://github.com/timeline.json")
print(r.text)               # 返回正常的网页内容, 即解压解码之后的内容
print(r.content)            # 返回byte类型的网页内容, 即值解压, 没有解码
print(r.json())             # 如果网页内容为json, 直接返回一个json对象
print(r.encoding)           # 返回网页的编码: "utf-8"

# Requests会自动解码来自服务器的内容, 也可以自己更改
r.encoding = "ISO-8859-1"
print(r.text)               # 此时使用新的r.encoding解码后的新值

# 编码的其他操作
# requests.utils.get_encodings_from_content(content): Returns encodings from given content string.
# requests.utils.get_encoding_from_headers(headers): Returns encodings from given HTTP Header Dict.
# requests.utils.get_unicode_from_response(r): Returns the requested content back in unicode.

# 原始响应内容: 获取来自服务器的原始套接字响应
r = requests.get("https://github.com/timeline.json", stream=True)
print(r.raw)                # <requests.packages.urllib3.response.HTTPResponse object at 0x101194810>
print(r.raw.read(10))       # "\x1f\x8b\x08\x00\x00\x00\x00\x00\x00\x03"

# 一般情况下, 应该以下面的模式将文本流保存到文件
with open("test", "wb") as fd:
    for chunk in r.iter_content(chunk_size=256):
        fd.write(chunk)
# 注意: 设置的timeout对connect和read起作用. 但一旦和服务器建立连接, r.content或r.iter_content就处于一个read的状态, 不受timeout影响

# 定制请求头: 一个字典
headers = {"user-agent": "my-app/0.0.1"}
r = requests.get("https://api.github.com/some/endpoint", headers=headers)
print(r.request.headers)    # 获取request的头部
print(r.headers)            # 获取response的头部
# {
#     "content-encoding": "gzip",
#     "transfer-encoding": "chunked",
#     "connection": "close",
#     "server": "nginx/1.0.4",
#     "x-runtime": "148ms",
#     "etag": "e1ca502697e5c9317743dc078f67693f",
#     "content-type": "application/json"
# }
print(r.headers["Content-Type"])        # "application/json"
print(r.headers.get("content-type"))    # "application/json"

# 更加复杂的POST请求: 表单
post_dict = {"key1": "value1", "key2": "value2"}
r = requests.post("http://httpbin.org/post", data=post_dict)
print(r.text)

# POST一个多部分编码(Multipart-Encoded)的文件
files = {"file": open("report.xls", "rb")}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)

# 你可以显式地设置文件名, 文件类型和请求头
files = {"file": ("report.xls", open("report.xls", "rb"), "application/vnd.ms-excel", {"Expires": "0"})}
r = requests.post("http://httpbin.org/post", files=files)
print(r.text)

# 你也可以发送文本字符串
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
bad_r.raise_for_status()                        # 引发异常

# Cookie: 如果某个响应中包含一些cookie, 则会被放到response.cookies(CookieJar类型)中
r = requests.get("http://example.com/some/cookie/setting/url")
print(r.cookies["example_cookie_name"])         # "example_cookie_value"

# 要想发送你的cookies到服务器, 可以使用cookies参数(一个字典)
cookies = dict(cookies_are="working")
r = requests.get("http://httpbin.org/cookies", cookies=cookies)
print(r.text)

# cookie的其他操作
# requests.utils.dict_from_cookiejar(cj): Returns a key/value dictionary from a CookieJar.
# requests.utils.cookiejar_from_dict(cookie_dict, cookiejar=None, overwrite=True): Returns a CookieJar from a key/value dictionary.
# requests.utils.add_dict_to_cookiejar(cj, cookie_dict): Returns a CookieJar from a key/value dictionary.

# 通用CookieJar类, 一个cookielib.CookieJar, 但是提供一个dict接口
# class requests.cookies.RequestsCookieJar(policy=None): Compatibility class; is a cookielib.CookieJar, but exposes a dict interface.

# 会话对象: 会话对象让你能够跨请求保持某些参数, 它也会在同一个Session实例发出的所有请求之间保持cookie
s = requests.Session()
s.get("http://httpbin.org/cookies/set/sessioncookie/123456789")
s.get("http://httpbin.org/cookies")
for cookie in s.cookies:
    print(cookie)

# 如果你要手动为会话添加cookie, 就是用Cookie utility函数来操纵Session.cookies
requests.utils.add_dict_to_cookiejar(s.cookies, {"cookie_key": "cookie_value"})

# 会话也可用来为请求方法提供缺省数据, 这是通过为会话对象的属性提供数据来实现的
s.auth = ("user", "pass")
s.headers.update({"x-test": "true"})
s.get("http://httpbin.org/headers", headers={"x-test2": "true"})        # both "x-test" and "x-test2" are sent

# 不过需要注意, 就算使用了会话, 方法级别的参数也不会被跨请求保持, 下面的例子只会给第一个请求发送cookie
s.get("http://httpbin.org/cookies", cookies={"from-my": "browser"})     # 带有cookie
s.get("http://httpbin.org/cookies")                                     # 不带cookie

# 会话还可以用作前后文管理器
with requests.Session() as s:
    s.get("http://httpbin.org/cookies/set/sessioncookie/123456789")
# class requests.Session类, 和requests外层有的函数/属性基本一致, 只不过是封装了一层跨域请求的功能

# 重定向与请求历史, 默认情况下, 除了HEAD, Requests会自动处理所有重定向, 可以通过allow_redirects参数禁用重定向处理
# 可以使用响应对象的history方法来追踪重定向, Response.history 是一个Response对象的列表, 按照从最老到最近的请求进行排序
r = requests.get("http://github.com", allow_redirects=True)
print(r.status_code)        # 200
print(r.history)            # [<Response [301]>]
r = requests.get("http://github.com", allow_redirects=False)
print(r.status_code)        # 301
print(r.history)            # []

# 超时, 设置timeout参数
requests.get("http://github.com", timeout=0.001)
# Traceback (most recent call last):
#   File "<stdin>", line 1, in <module>
# requests.exceptions.Timeout: HTTPConnectionPool(host="github.com", port=80): Request timed out. (timeout=0.001)

# 注意: timeout仅对连接过程有效, 与响应体的下载无关
# timeout并不是整个下载响应的时间限制, 而是如果服务器在timeout秒内没有应答, 将会引发一个异常
# 更精确地说, 是在timeout秒内没有从基础套接字上接收到任何字节的数据时
requests.get("https://github.com", timeout=5)

# 上边的timeout值将会用作 connect 和 read 二者的timeout, 如果要分别制定, 就传入一个元组
requests.get("https://github.com", timeout=(3.05, 27))

# 错误与异常: 遇到网络问题(如: DNS 查询失败、拒绝连接等)时, Requests 会抛出一个 ConnectionError 异常
# 如果 HTTP 请求返回了不成功的状态码, Response.raise_for_status() 会抛出一个 HTTPError 异常
# 若请求超时, 则抛出一个 Timeout 异常
# 若请求超过了设定的最大重定向次数, 则会抛出一个 TooManyRedirects 异常
# 所有Requests显式抛出的异常都继承自 requests.exceptions.RequestException

# 所有异常:
# exception requests.RequestException(*args, **kwargs): There was an ambiguous exception that occurred while handling your request.
# exception requests.ConnectionError(*args, **kwargs): A Connection error occurred.
# exception requests.HTTPError(*args, **kwargs): An HTTP error occurred.
# exception requests.URLRequired(*args, **kwargs): A valid URL is required to make a request.
# exception requests.TooManyRedirects(*args, **kwargs): Too many redirects.
# exception requests.ConnectTimeout(*args, **kwargs): The request timed out while trying to connect to the remote server.
# exception requests.ReadTimeout(*args, **kwargs): The server did not send any data in the allotted amount of time.
# exception requests.Timeout(*args, **kwargs): The request timed out.

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

# 除了基本的 HTTP 代理, Request 还支持 SOCKS 协议的代理, 此时需要单独安装:
# $ pip install requests[socks]
proxies = {
    "http": "socks5://user:pass@host:port",
    "https": "socks5://user:pass@host:port"
}
requests.get("http://example.org", proxies=proxies)

# Requests 传输适配器
# 从 v1.0.0 以后，Requests 的内部采用了模块化设计。部分原因是为了实现传输适配器（Transport Adapter）。
# 传输适配器提供了一个机制，让你可以为 HTTP 服务定义交互方法。尤其是它允许你应用服务前的配置。
# Requests 自带了一个传输适配器，也就是 HTTPAdapter。 这个适配器使用了强大的 urllib3，为 Requests 提供了默认的 HTTP 和 HTTPS 交互。
# 每当 Session 被初始化，就会有适配器附着在 Session 上，其中一个供 HTTP 使用，另一个供 HTTPS 使用。
# Request 允许用户创建和使用他们自己的传输适配器，实现他们需要的特殊功能。创建好以后，传输适配器可以被加载到一个会话对象上，附带着一个说明，告诉会话适配器应该应用在哪个 web 服务上。
s = requests.Session()
s.mount("http://baidu.com", requests.adapters.HTTPAdapter())

# 出现错误: Connection pool is full, discarding connection: xxxx.com
s.mount('https://', requests.adapters.HTTPAdapter(pool_connections=100, pool_maxsize=100))

# 关闭InsecurePlatformWarning
# requests.packages.urllib3.disable_warnings()
