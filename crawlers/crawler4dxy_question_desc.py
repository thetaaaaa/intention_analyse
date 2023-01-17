#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/8/12 11:59
# @Description:

import requests

session = requests.session()
headers = {
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Microsoft Edge";v="104"',
    'referer': 'https://www.dxy.cn/bbs/newweb/pc/post/31039763',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.81 Safari/537.36 Edg/104.0.1293.47',
    'cookie': 'JUTE_SESSION_ID=39892925-9fc5-4cce-a449-ad363ec7fc70; dxy_da_cookie-id=b244de42d0aaffd565183869b244b87a1660277068052; ifVisitOldVerBBS=false'

}
session.get("https://www.dxy.cn/bbs/newweb/pc/post/31039763", headers=headers)
u =  'https://www.dxy.cn/bbs/newweb/post/reply/tree-list?postId=31039763&pageNum=1&pageSize=20&orderType=3&onlyQuality=false&serverTimestamp=1660277069292&timestamp=1660277069503&noncestr=60577645&sign=37e1a65decf8df7afe1d431e9238770ef84369fe'
resp = session.get(u, headers=headers)
print(resp.text)
