#!/usr/bin/python

import requests
import proxy
import json


def agent_vin144_net(vinCode):
    home_url = "http://www.vin114.net/"
    post_url = "http://www.vin114.net/carpart/carmoduleinfo/vinresolve.jhtml"
    data_url = "http://www.vin114.net/visitor/carmoduleinfo/index.jhtml?levelIds=%s&vinDate=%s"
    timeout = 5
    try_count = 3
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


    for i in range(try_count):
        proxies = {
            "http": "http://%s"%(proxy.next_server())
        }
        try:
            response = None
            response = requests.get(home_url, proxies=proxies, timeout=timeout)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print "[1]", response
        if response.status_code == 200:
            break

    try:
        cookies =  response.cookies
    except UnboundLocalError:
        return html
    except AttributeError:
        return html

    payload = {'vinCode': vinCode}
    for i in range(try_count):
        try:
            response = None
            response = requests.post(post_url, proxies=proxies, timeout=timeout, data=payload, cookies=cookies, headers=headers_template)
        except requests.exceptions.ConnectTimeout:
            continue
        except requests.exceptions.ReadTimeout:
            continue
        except requests.exceptions.ConnectionError:
            continue

        print "[2]", response
        if response.status_code == 200:
            result = response.text
            break

    if result is not None:
        result = json.loads(result)
        print "result:", result
        if result["code"].startswith("S"):
            url = data_url % (result["message"]["levelIds"], result["message"]["vinDate"])

            for i in range(try_count):
                try:
                    response = None
                    response = requests.get(url, proxies=proxies, timeout=timeout)
                except requests.exceptions.ConnectTimeout:
                    continue
                except requests.exceptions.ReadTimeout:
                    continue
                except requests.exceptions.ConnectionError:
                    continue
    try:
        html = response.text
    except UnboundLocalError:
        pass

    return html


if __name__ == '__main__':
    print agent_vin144_net("LVSHCAMB1CE054249")
