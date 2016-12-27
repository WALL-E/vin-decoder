#!/usr/bin/python
# coding:utf-8
#
# 从Html文件中解析数据
#


import sys
import os
from bs4 import BeautifulSoup
import json

def parse_html_vin114_net(html):
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

    return json.dumps(result_dict, encoding='UTF-8', ensure_ascii=False)


def main():
    if len(sys.argv) < 2:
        print "./t.py filename.html"
        sys.exit(1)

    filename = sys.argv[1]
    if not os.path.exists(filename):
        print "%s is not exists" % (filename)
        sys.exit(1)
    html = open(filename)
    print parse_html_vin114_net(html)


if __name__ == "__main__":
    main()

