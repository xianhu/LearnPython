# _*_ coding: utf-8 _*_

"""
python_aiohttp.py by xianhu
"""

import asyncio
import aiohttp


# 简单实例
async def aiohttp_test01(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            print(resp.status)
            print(await resp.text())

loop = asyncio.get_event_loop()
tasks = [aiohttp_test01("https://api.github.com/events")]
loop.run_until_complete(asyncio.wait(tasks))
loop.close()

# 其他Http方法
# session.post('http://httpbin.org/post', data=b'data')
# session.put('http://httpbin.org/put', data=b'data')
# session.delete('http://httpbin.org/delete')
# session.head('http://httpbin.org/get')
# session.options('http://httpbin.org/get')
# session.patch('http://httpbin.org/patch', data=b'data')

# 自定义Headers
# payload = {'some': 'data'}
# headers = {'content-type': 'application/json'}
# await session.post(url, data=json.dumps(payload), headers=headers)

# 自定义Cookie
# cookies = {'cookies_are': 'working'}
# async with ClientSession(cookies=cookies) as session:
# 访问Cookie: session.cookie_jar

# 在URLs中传递参数
# 1. params = {'key1': 'value1', 'key2': 'value2'}
# 2. params = [('key', 'value1'), ('key', 'value2')]
# async with session.get('http://httpbin.org/get', params=params) as resp:
#     assert resp.url == 'http://httpbin.org/get?key2=value2&key1=value1'

# 发送数据
# payload = {'key1': 'value1', 'key2': 'value2'}
# async with session.post('http://httpbin.org/post', data=payload) as resp:
# async with session.post(url, data=json.dumps(payload)) as resp:
#     print(await resp.text())

# 发送文件(1)
# files = {'file': open('report.xls', 'rb')}
# await session.post(url, data=files)

# 发送数据(2)
# data = FormData()
# data.add_field('file',
#                open('report.xls', 'rb'),
#                filename='report.xls',
#                content_type='application/vnd.ms-excel')
# await session.post(url, data=data)

# 超时设置
# aync with session.get('https://github.com', timeout=60) as r:

# 代理支持
# async with aiohttp.ClientSession() as session:
#     async with session.get("http://python.org", proxy="http://some.proxy.com") as resp:
#         print(resp.status)

# async with aiohttp.ClientSession() as session:
#     proxy_auth = aiohttp.BasicAuth('user', 'pass')
#     async with session.get("http://python.org", proxy="http://some.proxy.com", proxy_auth=proxy_auth) as resp:
#         print(resp.status)
# session.get("http://python.org", proxy="http://user:pass@some.proxy.com")

# 返回的内容
# async with session.get('https://api.github.com/events') as resp:
#     print(await resp.text())
#     print(await resp.text(encoding='gbk'))
#     print(await resp.read())
#     print(await resp.json())

# 返回内容较大
# with open(filename, 'wb') as fd:
#     while True:
#         chunk = await resp.content.read(chunk_size)
#         if not chunk:
#             break
#         fd.write(chunk)

# 返回的其他变量
# async with session.get('http://httpbin.org/get') as resp:
#     print(resp.status)        # 状态码
#     print(resp.headers)       # Headers
#     print(resp.raw_headers)   # 原始Headers
#     print(resp.cookies)       # 返回的Cookie

# 访问历史History
# resp = await session.get('http://example.com/some/redirect/')
# resp: <ClientResponse(http://example.com/some/other/url/) [200]>
# resp.history: (<ClientResponse(http://example.com/some/redirect/) [301]>,)

# 释放返回的Response
# 1. async with session.get(url) as resp: pass
# 2. await resp.release()

# 连接器: Connectors
# conn = aiohttp.TCPConnector()
# session = aiohttp.ClientSession(connector=conn)

# 限制连接池大小:
# conn = aiohttp.TCPConnector(limit=30)
# conn = aiohttp.TCPConnector(limit=None)
