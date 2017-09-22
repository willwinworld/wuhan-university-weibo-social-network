#! python3
# -*- coding: utf-8 -*-
import json
import requests
from headers import headers
from pyquery import PyQuery as Pq
"""
cookie 24小时过期

"""
base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}&__rnd={}'


def send_request():
    with open('cookie.json', 'r') as f:
        cookie = json.loads(f.read())
    wei_bo_id = '4151542729073845'
    wei_bo_rnd = '1506047373356'
    specific_url = base_url.format(wei_bo_id, 1, wei_bo_rnd)
    r = requests.get(specific_url, headers=headers, verify=False, cookies=cookie)
    d = Pq(r.content).make_links_absolute(base_url=specific_url)
    total_page = d('.W_pages .page.S_txt1').eq(-1)

if __name__ == '__main__':
    send_request()


