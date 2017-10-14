#! python3
# -*- coding: utf-8 -*-
import re
import json
import time
import requests
from headers import headers
from fnvhash import fnv1a_32
from pyquery import PyQuery as Pq
from peewee import IntegrityError
from random import randint
from logger.log import crawler, parser, other, storage


with open('cookie.json', 'r') as f:
    cookie = json.loads(f.read())
s = requests.Session()


# base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}&__rnd={}'
# another_url = '/aj/v6/comment/big?ajwvr=6&id=4151542729073845&root_comment_max_id=4154068584896369&root_comment_max_id_type=&root_comment_ext_param=&page=2&filter=all&sum_comment_number=15&filter_tips_before=0&from=singleWeiBo&__rnd=1507973354180'
base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&root_comment_max_id={}&page={}&__rnd={}'

mid = '4151542729073845'
max_mid = '4154068584896369'
cur_time = int(time.time() * 1000)


# test_url = new_url.format(mid, max_mid, 1, cur_time)
# response = s.get(test_url, headers=headers, verify=False, cookies=cookie)
# test_data = response.content
# print(test_data)


class Comment(object):
    @classmethod
    def page_one(cls):
        """
        获取评论第一页的内容，返回第一页的内容，还有总的页数
        :return:
        """
        start_url = base_url.format(mid, max_mid, 1, cur_time)
        response = s.get(start_url, headers=headers, verify=False, cookies=cookie)
        crawler.warning(response.content)
        parse_able_data = json.loads(response.content)
        total_page = parse_able_data['data']['page']['totalpage']
        crawler.warning(total_page)
        current_page_num = parse_able_data['data']['page']['pagenum']
        crawler.warning(current_page_num)
        page_one_raw_html = parse_able_data['data']['html']
        return total_page, current_page_num, page_one_raw_html

    @classmethod
    def

