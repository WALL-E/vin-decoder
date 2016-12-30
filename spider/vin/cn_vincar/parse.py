#!/usr/bin/python
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
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')

        for table in tables:
            result = {}
            for row in table.findAll('tr')[:-1]:
                ths = row.findAll("th")
                tds = row.findAll("td")
                for i in range(2):
                    result[ths[i].string] = tds[i].string
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
    html = open(filename)
    data = parse_html(html)
    print "result:", json.dumps(data, encoding='UTF-8', ensure_ascii=False)


if __name__ == "__main__":
    main()
