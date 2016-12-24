#!/usr/bin/python

# -*- coding: UTF-8 -*-

import sys
import os
import requests
import ipaddress
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../rabbitmq'))

from rabbitmq import RabbitMQ

timeout = 5
headers_default = {
    "Pragma": "no-cache",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
}

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.findAll('table')
    table = tables[2]
    mq = RabbitMQ(queue="66ip")
    for tr in table.findAll('tr')[1:]:
        tds = tr.findAll('td')
        if len(tds) > 0:
            ip = tds[0].string
            port = tds[1].string
            content = "%s:%s" %(ip, port)
            print content
            try:
                ip_tmp = ipaddress.IPv4Address(ip.decode("utf-8"))
                if ip_tmp.is_private or ip_tmp.is_reserved or ip_tmp.is_multicast:
                    print "private,reserved,multicast is not valid"
                    continue
            except ipaddress.AddressValueError, msg:
                print msg
                continue
            mq.publish(content)

def get_page(url):
    response = requests.get(url, headers=headers_default, timeout=timeout)
    return response.text


def main():
    home_url = "http://www.66ip.cn/areaindex_1/1.html"
    html = get_page(home_url)
    parse_html(html)

if __name__ == '__main__':
    main()
