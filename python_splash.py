# _*_ coding: utf-8 _*_

"""
使用Splash服务器抓取Ajax渲染页面
"""

import json
import requests

# Docker安装: https://splash.readthedocs.io/en/latest/install.html
CRAWLER_URL = "http://weixin.sogou.com/weixin?page=1&type=2&query=%E4%B8%AD%E5%9B%BD"


# render.html
def test_1(url):
    render = "http://xx.xx.xx.xx:8050/render.html"
    body = json.dumps({
        "url": url,
        "wait": 0.5,                                # 设定页面加载等待时间
        "images": 0,                                # 是否抓取图片
        "timeout": 3,                               # 设置过期时间
        # "allowed_domains": ["sogou.com", ],       # 设置允许的域
        "allowed_content_types": "text/html; charset=utf-8"
    })
    headers = {"Content-Type": "application/json"}

    response = requests.post(url=render, headers=headers, data=body)
    print(url, response.status_code)
    print(response.text)
    return

# test_1(CRAWLER_URL)


# render.png
def test_2(url):
    render = "http://xx.xx.xx.xx:8050/render.png?url=%s&timeout=5" % url
    response = requests.get(url=render)
    print(url, response.status_code)
    return

# test_2(CRAWLER_URL)
