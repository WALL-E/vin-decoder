#!/usr/bin/env python
# coding:utf-8
"""
模拟用户提交请求
"""

import copy
import sys
import os
import time

from bs4 import BeautifulSoup
import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../../proxy'))

import proxy

HOME_URL = "https://vincar.cn/"
POST_URL = "https://vincar.cn/vin"

HEADERS_GET = {
    "Pragma": "no-cache",
    "Accept-Encoding": "gzip, deflate, sdch, br",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}
HEADERS_POST = {
    "Pragma": "no-cache",
    "Origin": "https://vincar.cn",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "https://vincar.cn/",
}

TIMEOUT = 5
TRY_COUNT = 10

def robot_html(vin_code, proxy_use=True, proxy_reuse=False):
    """
    模拟用户提交网页POST请求

    :param vin_code:    string, vin code
    :param proxy_use:   bool
    :param proxy_reuse: bool
    :returns: string or None
    """
    html = None
    # 1-Request
    response = None
    cookies = None
    for _ in range(TRY_COUNT):
        proxies = {}
        if proxy_use:
            print "use proxy to post data"
            server = proxy.next_server()
            if server is None:
                print "No agents available, wating 60s"
                time.sleep(60)
                continue
            proxies["http"] = "http://%s" % (server)
        try:
            response = requests.get(HOME_URL, proxies=proxies, timeout=TIMEOUT, headers=HEADERS_GET, verify=False)
        except Exception, msg:
            print msg
            continue

        print "[1]", response
        if response is not None and response.status_code == 200:
            if proxy_use and proxy_reuse:
                proxy.requeue_server(server)
            cookies = response.cookies
            break

    if response is None:
        print "No agents available, retry %s" % (TRY_COUNT)
        return html

    # Get CSRF Token
    soup = BeautifulSoup(response.text.encode(response.encoding), "html.parser")
    tokens = soup.findAll('meta', {"name": "csrf-token"})
    token = tokens[0].attrs["content"]
    headers = copy.deepcopy(HEADERS_POST)
    headers["X-CSRF-Token"] = token


    # 2-Request
    payload = {'vin': vin_code}
    response = None
    for _ in range(1):
        try:
            response = requests.post(POST_URL, proxies=proxies, timeout=TIMEOUT, data=payload, cookies=cookies, headers=headers, verify=False)
        except Exception, msg:
            print msg
            continue

        print "[2]", response
        if response.status_code == 200:
            html = response.text.encode(response.encoding)
            break

    return html


if __name__ == '__main__':
    print robot_html("LVSHCAMB1CE054249", proxy_use=True, proxy_reuse=True)
