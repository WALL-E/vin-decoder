#!/usr/bin/env python2.7
# coding:utf-8
"""
模拟用户提交请求
"""

import sys
import os
import time

import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../..'))

from proxy import proxy

URL = "http://spider.51kahui.com/CarInfo/vinQuery"
TIMEOUT = 60
TRY_COUNT = 10

def robot_html(vin_code, proxy_use=True, proxy_reuse=False):
    """
    模拟用户提交网页POST请求

    :param vin_code:    string, vin code
    :returns: string or None
    """
    html = None
    # 1-Request
    response = None
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
            payload = {"vinCode": vin_code}
            response = requests.post(URL, proxies=proxies, timeout=TIMEOUT, data=payload)
        except Exception, msg:
            print msg
            continue

        print "[1]", response
        if response is not None and response.status_code == 200:
            if proxy_use and proxy_reuse:
                proxy.requeue_server(server)
            html = response.text.encode(response.encoding)
            break

    if response is None:
        print "No agents available, retry %s" % (TRY_COUNT)
        return html

    return html


if __name__ == '__main__':
    print robot_html("LVSHCAMB1CE054249", proxy_use=False, proxy_reuse=False)
