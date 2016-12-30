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
    parse html of http://www.vin114.net/

    :param html: html strings
    :returns: list
    """
    results = []
    try:
        soup = BeautifulSoup(html, "html.parser")
        tables = soup.findAll('table')
        table = tables[0]

        tmp_list = []
        for row in table.findAll('tr'):
            for child in row.children:
                ret = child.string.strip()
                if len(ret) > 0:
                    tmp_list.append(ret.encode("utf8"))

        tmp_dict = {}
        for i in range(0, len(tmp_list), 2):
            key = tmp_list[i]
            val = tmp_list[i+1]
            tmp_dict[key] = val
        results.append(tmp_dict)
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
