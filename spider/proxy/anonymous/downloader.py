#!/usr/bin/python

# -*- coding: UTF-8 -*-

import sys
import os
import time
import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../../rabbitmq'))
sys.path.append(os.path.join(ROOT_DIR, '../../../proxy'))

import proxy

timeout = 10
try_count = 10
headers_default = {
    "Pragma": "no-cache",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}

def get_page(url):
    response = None
    html = None
    for i in range(try_count):
        print "try again: %s" % (i)
        server = proxy.next_server()
        if server is None:
            print "No agents available"
            time.sleep(60)
            continue
        proxies = {
            "http": "http://%s" % (server)
        }
        try:
             response = requests.get(url, headers=headers_default, timeout=timeout, proxies=proxies)
        except requests.exceptions.ConnectTimeout, msg:
            print msg
            continue
        except requests.exceptions.ReadTimeout, msg:
            print msg
            continue
        except requests.exceptions.ConnectionError, msg:
            print msg
            continue
        if response is not None and response.status_code == 200:
            html = response.text
            break
        else:
            print "response:", response
    return html


def main():
    home_url = "http://api.ffan.com/"
    html = get_page(home_url)
    print html

if __name__ == '__main__':
    main()
