#! python3
# -*- coding: utf-8 -*-
import json
import requests
from headers import headers

wei_bo_start_rnd = '1506222109180'
# test = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4151542729073845&__rnd=1506222109180'
try_out_url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4151542729073845&__rnd=1506224068615'
turn_page_url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4151542729073845&max_id=4155177487146495&page=2&__rnd=1506225380928'
new_url = 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4151542729073845&max_id=4155177487146495&page=2&__rnd=1506224068615'
with open('cookie.json', 'r') as f:
    cookie = json.loads(f.read())
s = requests.Session()
response = s.get('https://weibo.com/5861369000/FlCRqC4wl?type=repost#_rnd1506224396841', headers=headers, verify=False, cookies=cookie)
print(response.content)


# 'https://weibo.com/aj/v6/mblog/info/big?ajwvr=6&id=4151542729073845&__rnd=1506224068615'