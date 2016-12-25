#!/usr/bin/python

import sys
import os
import requests
import json
import time
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../../proxy'))

import proxy


def robot_html(vinCode):
    home_url = "https://vincar.cn/"
    post_url = "https://vincar.cn/vin"
    timeout = 5
    try_count = 10
    html = None
    result = None
    headers_template = {
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

    # 1-Request
    response_1 = None
    cookies = None
    for i in range(try_count):
        server = proxy.next_server()
        if server is None:
              print "No agents available"
              time.sleep(60)
              continue
        proxies = {
            "http": "http://%s" % (server)
        }
        try:
            response_1 = requests.get(home_url, proxies=proxies, timeout=timeout, verify=False)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print "[1]", response_1
        if response_1 is not None and response_1.status_code == 200:
            proxy.requeue_server(server)
            cookies = response_1.cookies
            break

    if response_1 is None:
        print "No agents available"
        return html

    soup = BeautifulSoup(response_1.text, "html.parser")
    tokens = soup.findAll('meta', {"name": "csrf-token"})
    token = tokens[0].attrs["content"]
    headers_template["X-CSRF-Token"] = token

    # 2-Request
    payload = {'vin': vinCode}
    response_2 = None
    for i in range(try_count):
        try:
            response_2 = requests.post(post_url, proxies=proxies, timeout=timeout, data=payload, cookies=cookies, headers=headers_template, verify=False)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print "[2]", response_2.text
        if response_2.status_code == 200:
            html = response_2.text
            break

    return html


if __name__ == '__main__':
    print robot_html("LVSHCAMB1CE054249")
