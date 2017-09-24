#! python3
# -*- coding: utf-8 -*-
import re
import json
import requests
from headers import headers
from pyquery import PyQuery as Pq
from peewee import IntegrityError
from db.weibo_repost import Original_Weibo_Repost
from db.weibo_repost_basic_parse_res import Basic_Weibo_Repost_Parse_Res
from logger.log import crawler, parser, other, storage
"""
对已保存到数据库的文本进行处理
1.先进行非结构化到结构化处理，将一整页的html拆成一个个评论
"""


def process_raw_data():
    fetch_from_database = []
    for row in Original_Weibo_Repost.select():
        current_page = row.current_page
        crawler.warning(current_page)
        raw_html = row.raw_html
        d = Pq(raw_html)
        repost_list = [{'current_page': current_page, 'mid_id': i.attr('mid'), 'repost_html': i.html()} for i in d('.list_li.S_line1.clearfix').items()]
        fetch_from_database.extend(repost_list)
    # print(fetch_from_database[-1])
    # print(len(fetch_from_database))

    basic_parse_res = []  # 第一层的解析结果
    for i in fetch_from_database:
        current_page = i['current_page']
        crawler.warning(current_page)
        mid_id = i['mid_id']
        crawler.warning(mid_id)
        repost_html = i['repost_html']
        d = Pq(repost_html)
        repost_user_id = re.findall(r'\d+', d('.WB_face.W_fl a img').attr('usercard'))[0]  # 用户id
        crawler.warning(repost_user_id)
        repost_content = d('.WB_text span').text()  # 转发评论
        crawler.warning(repost_content)
        repost_time = d('.WB_from.S_txt2').text()  # 转发时间
        crawler.warning(repost_time)
        repost_list = re.findall(r'\d+', d('.WB_func.clearfix .WB_handle.W_fr .clearfix li:eq(1) .line.S_line1 .S_txt1').text())  # 转发数
        repost_num = 0
        upvote_num = 0
        if len(repost_list) != 0:
            repost_num = repost_list[0]
        upvote_list = re.findall(r'\d+', d('.WB_func.clearfix .WB_handle.W_fr .clearfix li:eq(2) .line.S_line1 a span em:eq(1)').text())  # 点赞数
        if len(upvote_list) != 0:
            upvote_num = upvote_list[0]
        crawler.warning(repost_num)
        crawler.warning(upvote_num)
        basic_parse_res.append({'current_page': current_page, 'mid_id': mid_id, 'repost_html': repost_html,
                                'repost_user_id': repost_user_id, 'repost_content': repost_content,
                                'repost_time': repost_time, 'repost_num': repost_num, 'upvote_num': upvote_num})
    return basic_parse_res


def save(basic_parse_res):
    for single_res in basic_parse_res:
        try:
            Basic_Weibo_Repost_Parse_Res.create(id=int(single_res['mid_id']),
                                                current_page=single_res['current_page'],
                                                mid_id=int(single_res['mid_id']),
                                                repost_html=single_res['repost_html'],
                                                repost_user_id=int(single_res['repost_user_id']),
                                                repost_content=single_res['repost_content'],
                                                repost_time=single_res['repost_time'],
                                                repost_num=int(single_res['repost_num']),
                                                upvote_num=int(single_res['upvote_num']))
        except IntegrityError as err:
            crawler.warning(err)


def combine():
    basic_parse_res = process_raw_data()
    save(basic_parse_res)


# if __name__ == '__main__':
#     combine()


__all__ = ['combine']