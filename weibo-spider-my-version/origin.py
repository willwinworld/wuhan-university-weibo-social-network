#! python3
# -*- coding: utf-8 -*-
import json
import requests
from headers import headers
from peewee import IntegrityError
from db.weibo_repost import Original_Weibo_Repost
from logger.log import crawler, parser, other, storage
"""
cookie 24小时过期
同时如果用同一个账号的cookie经常访问页面过久，请求获得的是空的页面
"""
base_url = 'http://weibo.com/aj/v6/comment/big?ajwvr=6&id={}&page={}&__rnd={}'  # rnd是过期时间
wei_bo_start_id = '4151542729073845'
wei_bo_start_rnd = '1506224068615'
with open('cookie.json', 'r') as f:
    cookie = json.loads(f.read())
s = requests.Session()


def send_start_request():
    specific_url = base_url.format(wei_bo_start_id, 1, wei_bo_start_rnd)
    response = s.get(specific_url, headers=headers, verify=False, cookies=cookie)
    crawler.warning(response.content)
    parse_able_data = json.loads(response.content)   # 解析成python内置数据结构
    total_page = parse_able_data['data']['page']['totalpage']  # 总的页面
    crawler.warning(total_page)
    page_one_current_page = parse_able_data['data']['page']['pagenum']  # 当前页面
    crawler.warning(page_one_current_page)
    page_one_raw_html = parse_able_data['data']['html']  # 第一页的html

    # s.cookies.set(**cookie)
    # response = s.get(specific_url, headers=headers, verify=False)
    # print(response.content)
    # r = requests.get(specific_url, headers=headers, verify=False, cookies=cookie)
    # print(r.content)
    # r = requests.get(specific_url, headers=headers, verify=False, cookies=cookie)
    # print(r.content)
    # d = Pq(response.content).make_links_absolute(base_url=specific_url)
    # total_page = d('.W_pages .page.S_txt1').eq(-1).text()
    # print(total_page)
    # page_one_repost_html = [i.html() for i in d('.repeat_list .list_box .list_ul .list_li.S_line1.clearfix').items()]
    # print(page_one_repost_html)
    return total_page, page_one_current_page, page_one_raw_html


def send_rest_request(total_page):
    generate_url = []
    int_total_page = int(total_page)
    for i in range(2, int_total_page+1):
        generate_url.append(base_url.format(wei_bo_start_id, i, wei_bo_start_rnd))
    rest_res = []
    for i_url in generate_url:
        response = s.get(i_url, headers=headers, verify=False, cookies=cookie)
        crawler.warning(i_url)
        parse_able_data = json.loads(response.content)
        i_current_page = parse_able_data['data']['page']['pagenum']
        crawler.warning(i_current_page)
        i_raw_html = parse_able_data['data']['html']
        rest_res.append({'current_page': i_current_page, 'raw_html': i_raw_html})
        break
    return rest_res


def save(page_one_current_page, page_one_raw_html, rest_res):
    total_res = []
    first_res = {'current_page': page_one_current_page, 'raw_html': page_one_raw_html}
    total_res.insert(0, first_res)
    total_res.extend(rest_res)

    for single_res in total_res:
        try:
            Original_Weibo_Repost.create(id=single_res['current_page'],
                                         current_page=single_res['current_page'],
                                         raw_html=single_res['raw_html'])
        except IntegrityError as err:
            pass


def combine():
    total_page, page_one_current_page, page_one_raw_html = send_start_request()
    # print(total_page)
    # print(page_one_current_page)
    # print(page_one_raw_html)
    rest_res = send_rest_request(total_page)
    save(page_one_current_page, page_one_raw_html, rest_res)


if __name__ == '__main__':
    combine()


# __all__ = ['combine']
