#!/usr/bin/python

import requests
import proxy
import json


def robot_html_vin144_net(vinCode):
    home_url = "http://www.vin114.net/"
    post_url = "http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml"
    data_url = "http://www.vin114.net/visitor/carmoduleinfo/index.jhtml?levelIds=%s&vinDate=%s"
    timeout = 5
    try_count = 10
    html = None
    result = None
    headers_template = {
        "Pragma": "no-cache",
        "Origin": "http://www.vin114.net",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6,ja;q=0.4",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Cache-Control": "no-cache",
        "X-Requested-With": "XMLHttpRequest",
        "Connection": "keep-alive",
        "Referer": "http://www.vin114.net/",
    }

    # 1-Request
    response_1 = None
    cookies = None
    for i in range(try_count):
        proxies = {
            "http": "http://%s"%(proxy.next_server())
        }
        try:
            response_1 = requests.get(home_url, proxies=proxies, timeout=timeout)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print "[1]", response_1
        if response_1 is not None and response_1.status_code == 200:
            cookies = response_1.cookies
            break

    if response_1 is None:
        print "No agents available"
        return html

    # 2-Request
    payload = {'vinCode': vinCode}
    response_2 = None
    url = None
    for i in range(try_count):
        try:
            response_2 = requests.post(post_url, proxies=proxies, timeout=timeout, data=payload, cookies=cookies, headers=headers_template)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print "[2]", response_2
        if response_2.status_code == 200:
            result = response_2.text
            result = json.loads(result)
            print "[2] result:", json.dumps(result, encoding='UTF-8', ensure_ascii=False)
            if result["code"].startswith("S") and result["code"] != "S0":
                url = data_url % (result["message"]["levelIds"], result["message"]["vinDate"])
            break

    if response_2 is None or url is None:
        return html

    # 3-Request
    response_3 = None
    for i in range(try_count):
        try:
            response_3 = requests.get(url, proxies=proxies, timeout=timeout)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

    if response_3 is not None:
        html = response_3.text

    return html


if __name__ == '__main__':
    print robot_html_vin144_net("LVSHCAMB1CE054249")
