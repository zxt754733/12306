# -*- coding: utf-8 -*-
"""
Created on 2019/1/23 16:51
Author  : zxt
File    : get_ip.py
Software: PyCharm
"""

import requests
from pyquery import PyQuery as pq


def get_effective_ip():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/69.0.3497.100 Safari/537.36'
    }
    effective_ip = []
    url = 'https://www.xicidaili.com/nn/'
    response = requests.session().get(url, headers=headers)
    print(response.status_code)
    doc = pq(response.text)
    for item in doc('#ip_list tr').items():
        ip = item('td').eq(1).text()
        port = item('td').eq(2).text()
        # print(item('td').eq(5))
        if ip != '' and port != '':
            proxies = {item('td').eq(5).text().lower(): item('td').eq(5).text().lower() + '://' + ip + ':' + port}
            try:
                if requests.session().get(
                        'https://www.12306.cn/index/index.html', proxies=proxies, headers=headers
                ).status_code == 200:
                    effective_ip.append(proxies)
                    print('effective: ', proxies)
                    if item('td').eq(5).text().lower() == 'https':
                        response = requests.session().get(
                                'https://www.12306.cn/index/index.html', proxies=proxies, headers=headers
                            )
                        response.encoding = 'utf-8'
                        print(
                            response.text
                        )
                else:
                    continue
            except:
                print('invalid:', proxies)
                continue


if __name__ == '__main__':
    get_effective_ip()
