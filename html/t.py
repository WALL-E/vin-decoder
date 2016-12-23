#!/usr/bin/python
# coding:utf-8
#
# 从Html中解析数据
#


from bs4 import BeautifulSoup
import json

def parse_vin114_net():
    soup = BeautifulSoup(open('LVSHCAMB1CE054249.html'), "html.parser")

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
    print parse_vin114_net()


if __name__ == "__main__":
    main()

