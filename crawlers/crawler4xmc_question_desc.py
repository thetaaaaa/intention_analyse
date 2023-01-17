#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/8/11 21:47 
# @Description:
import time
import requests
import re
import pandas as pd
import os
import logging
import random

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO,
                    filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/xmcCrawler.log", encoding='utf-8')
logger.addHandler(handler)

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                        'Chrome/86.0.4240.75 Safari/537.36'}


def get_desc(url):
    response = requests.get(url, headers=header, timeout=100)
    desc = re.findall('<meta name="description" content="(.+?)">', response.text)[0]
    return desc


xmc = pd.read_excel('data/小木虫论坛-论文投稿-仅投稿求助-20220810采集.xlsx')
urls = xmc['link'].values.tolist()
xmc = pd.concat([xmc, pd.DataFrame(columns=['desc'])])
error_urls = []
for idx, url in enumerate(urls):
    try:
        desc = get_desc(url)
        xmc.iloc[idx, 5] = desc
        logger.info('{},{},{}'.format(idx, url, desc))
        time.sleep(random.uniform(1, 3.8))
    except Exception:
        xmc.to_csv('../data/xmc.tsv', sep='\t', index=False)
        error_urls.append([idx, url])
        pd.DataFrame(error_urls, columns=['index', 'link']).to_csv('log/urls_need_retry.tsv', sep='\t')

xmc.to_csv('data/xmc.tsv', sep='\t', index=False)
pd.DataFrame(error_urls, columns=['index', 'link']).to_csv('log/urls_need_retry.tsv', sep='\t')
