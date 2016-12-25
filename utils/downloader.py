#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
downloader: get_page
"""

import os
import sys
import time

import requests

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../proxy'))

import proxy

TIMEOUT = 10
TRY_COUNT = 10
HEADERS_GET = {
    "Pragma": "no-cache",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}


def get_page(url, proxy_use=True, proxy_reuse=False):
    """
    下载网页

    :param url:    string, url
    :returns: string or None
    """
    response = None
    html = None
    for i in range(TRY_COUNT):
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
            response = requests.get(url, headers=HEADERS_GET, timeout=TIMEOUT, proxies=proxies)
        except Exception, msg:
            print msg
            continue

        print "response:", response
        if response is not None and response.status_code == 200:
            html = response.text
            if proxy_use and proxy_reuse:
                proxy.requeue_server(server)
            break
    return html


def main():
    """
    main function
    """
    home_url = "http://api.ffan.com/"
    html = get_page(home_url, proxy_use=True, proxy_reuse=False)
    print html

if __name__ == '__main__':
    main()
