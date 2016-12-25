#!/usr/bin/python

# -*- coding: UTF-8 -*-

import sys
import os
import time
import ipaddress
from bs4 import BeautifulSoup

ROOT_DIR = os.path.dirname(__file__)
sys.path.append(ROOT_DIR)
sys.path.append(os.path.join(ROOT_DIR, '../../rabbitmq'))
sys.path.append(os.path.join(ROOT_DIR, '../../utils'))

from rabbitmq import RabbitMQ
from downloader import get_page


def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    tables = soup.findAll('table')
    table = tables[0]
    mq = RabbitMQ(queue="31f")
    for tr in table.findAll('tr')[1:]:
        tds = tr.findAll('td')
        if len(tds) > 0:
            ip = tds[1].string
            port = tds[2].string
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


def main():
    home_url = "http://31f.cn/http-proxy/"

    while True:
        html = get_page(home_url, proxy_use=False)
        parse_html(html)
        time.sleep(300)

if __name__ == '__main__':
    main()
