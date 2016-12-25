#!/usr/bin/python
# coding:utf-8
#
# 从Html文件中解析数据
#


import sys
import os
from bs4 import BeautifulSoup
import json


def to_json(obj):
    return json.dumps(obj, encoding='UTF-8', ensure_ascii=False)


def parse_html(html):
    """
    parse html of vin114.net

    :param html: html strings
    :returns: dict or None
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        
        results = []
        for table in tables:
            result = {}
            for row in table.findAll('tr')[:-1]:
                ths = row.findAll("th")
                tds = row.findAll("td")
                for i in (0,1):
                    result[ths[i].string] = tds[i].string
            results.append(result)
        return results
    except Exception, msg:
        print "error: [parse html] %s" % (msg)
        return None


def main():
    if len(sys.argv) < 2:
        print "%s filename.html" % (sys.argv[0])
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print "%s is not exists" % (filename)
        sys.exit(1)
    html = open(filename)
    data = parse_html(html)
    if data is None:
        print "result:", data
    else:
        print "result:", json.dumps(data, encoding='UTF-8', ensure_ascii=False)


if __name__ == "__main__":
    main()

