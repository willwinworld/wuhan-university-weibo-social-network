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
开始根据是否有转发数来进行递归抓取
"""