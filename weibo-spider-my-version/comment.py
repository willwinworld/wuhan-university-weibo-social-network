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
    def parse_page_one(cls):
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
    def parse_page_rest(cls, total_page):
        generate_url = []
        int_total_page = int(total_page)
        for i in range(2, int_total_page + 1):
            generate_url.append(base_url.format(mid, max_mid, i, cur_time))
            break
        rest_res = []
        for i in generate_url:
            response = s.get(i, headers=headers, verify=False, cookies=cookie)
            crawler.warning(i)
            parse_able_data = json.loads(response.content)
            current_page = parse_able_data['data']['page']['pagenum']
            crawler.warning(current_page)
            raw_html = parse_able_data['data']['html']
            rest_res.append({'current_page': current_page, 'raw_html': raw_html})
            break
        return rest_res

    @classmethod
    def merge(cls, page_one_raw_html, rest_res):
        total_raw_res = []
        total_raw_res.insert(0, {'current_page': '1', 'raw_html': page_one_raw_html})
        total_raw_res.extend(rest_res)
        return total_raw_res

    @classmethod
    def parse_all(cls, total_raw_res):
        for item in total_raw_res:
            current_page = item['current_page']
            raw_html = item['raw_html']
            print(raw_html)
            d = Pq(raw_html)
            """
                ->
            map->
                ->
            """
            
            break

    @staticmethod
    def main():
        total_page, current_page_num, page_one_raw_html = Comment.parse_page_one()
        rest_res = Comment.parse_page_rest(total_page)
        total_raw_res = Comment.merge(page_one_raw_html, rest_res)
        Comment.parse_all(total_raw_res)


if __name__ == '__main__':
    Comment.main()

