#!/usr/bin/env python2.7
# coding:utf-8
"""
从Html文件中解析车辆信息
"""

import sys
import os
import json

from bs4 import BeautifulSoup


def parse_html(html):
    """
    parse html of https://vincar.cn/

    :param html: html strings
    :returns: list
    """
    results = []
    try:
        data = json.loads(html)
        print data
        if data["status"] == "20000000":
            result = data["result"]
            results.append(result)
    except Exception, msg:
        print "error: [parse html] %s" % (msg)
    return results


def main():
    """
    main function
    """
    if len(sys.argv) < 2:
        print "%s filename.html" % (sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print "%s is not exists" % (filename)
        sys.exit(1)
    html = open(filename).readline().strip()
    data = parse_html(html)
    print "result:", json.dumps(data, encoding='UTF-8', ensure_ascii=False)


if __name__ == "__main__":
    main()
