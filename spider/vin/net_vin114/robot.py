#!/usr/bin/env python2.7
# coding:utf-8
"""
模拟用户提交请求
"""

import sys
import os
import json
import time

import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../..'))

from proxy import proxy

HOME_URL = "http://www.vin114.net/"
POST_URL = "http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml"
DATA_URL = "http://www.vin114.net/visitor/carmoduleinfo/index.jhtml?levelIds=%s&vinDate=%s"

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
    "Origin": "http://www.vin114.net",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Cache-Control": "no-cache",
    "X-Requested-With": "XMLHttpRequest",
    "Connection": "keep-alive",
    "Referer": "http://www.vin114.net/",
}


TIMEOUT = 10
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
    result = None
    # 1-Request
    response = None
    cookies = None
    for _ in range(TRY_COUNT):
        proxies = {}
        if proxy_use:
            print "use proxy to post data"
            server = proxy.next_server()
            if server is None:
                print "No agents available"
                time.sleep(60)
                continue
            proxies["http"] = "http://%s" % (server)
        try:
            response = requests.get(HOME_URL, proxies=proxies, timeout=TIMEOUT, headers=HEADERS_GET)
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
        print "[1]No agents available or Timeout"
        return html

    # 2-Request
    payload = {'vinCode': vin_code}
    response = None
    url = None
    for i in range(1):
        try:
            response = requests.post(POST_URL, proxies=proxies, timeout=TIMEOUT, data=payload, cookies=cookies, headers=HEADERS_POST)
        except Exception, msg:
            print msg
            continue

        print "[2]", response
        if response.status_code == 200:
            result = response.text.encode(response.encoding)
            result = json.loads(result)
            print "[2] result: %s" % (result)
            if result["code"].startswith("S") and result["code"] != "S0":
                url = DATA_URL % (result["message"]["levelIds"], result["message"]["vinDate"])
            break

    if response is None or url is None:
        print "[2]No agents available or Timeout or Be restricted"
        return html

    # 3-Request
    response = None
    for i in range(1):
        try:
            response = requests.get(url, proxies=proxies, timeout=TIMEOUT)
        except Exception, msg:
            print msg
            continue

    if response is not None:
        html = response.text.encode(response.encoding)

    return html


if __name__ == '__main__':
    print robot_html("LVSHCAMB1CE054249", proxy_use=True, proxy_reuse=False)
