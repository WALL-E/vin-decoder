#!/usr/bin/python
# coding:utf-8
#
# 从Html文件中解析数据
#


import sys
import os
from bs4 import BeautifulSoup
import json

def parse_html(html):
    """
    parse html of vin114.net

    :param html: html strings
    :returns: dict or None
    """
    try:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        table = tables[0]

        result_list = []
        for row in table.findAll('tr'):
            for child in row.children:
                ret = child.string.strip()
                if len(ret) > 0:
                    result_list.append(ret.encode("utf8"))

        result_dict = {}
        for i in range(0, len(result_list), 2):
            k = result_list[i]
            v = result_list[i+1]
            result_dict[k] = v

        return result_dict
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

