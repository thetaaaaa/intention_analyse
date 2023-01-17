#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/8/8 21:59 
# @Description: 清洗学术社区提问文本数据
import unicodedata
import pandas as pd
import os, re
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO,
                    filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log/clean.log", encoding='utf-8')
logger.addHandler(handler)


def beacon_dect(sen):
    beacon = ['欢迎', '祈福', '祝福', '散花', '散金', '撒花', '删帖', '本贴内容被屏蔽', '屏蔽']  # xmc
    for i in beacon:
        if i in sen:
            return False
    return True


def clean_sentence(x):
    # x = unicodedata.normalize('NFKC', str(x))  # 将异常unicode字符转为正常字符
    x = str(x)
    x = re.sub('论文投稿 投稿求助|小木虫 论坛', '', x)
    x = re.sub('(如题|rt)[！!,，。.？?]+', '', x)
    x = re.sub('(如题|rt)', '', x)
    x = re.sub('(谢谢|很急|急)[！!,，。.？?]+', '', x)
    x = re.sub('(急)+[！!,，。.？?]', '', x)
    x = re.sub('[\-]+', '', x)
    x = x.replace('.....', '')
    x = re.sub('\n', '', x)
    x = re.sub('【.+?】', '', x)
    x = re.sub('\[.+?\]', '', x)
    x = re.sub('\ufeff|&amp;|#128532;', '', x)
    x = re.sub('(https?|ftp|file)://[-A-Za-z0-9+&@#/%?=~_|!:,.;]+[-A-Za-z0-9+&@#/%=~_|]', '', x)  # 清除网址
    x = x.strip(' ').strip('\n')
    # x = ''.join(re.findall('[^\x00-\xff]+', x))  # 去除非汉语内容
    return x


def clean_xmc():  # 清洗小木虫提问文本
    beacon = ['求好运', '欢迎', '祈福', '祝福', '散花', '散金', '撒花', '删帖', '本贴内容被屏蔽', '屏蔽', '金币',
              '还愿', '投稿顺利', '论文集福', '祈祷', '撒币']
    raw_data = pd.read_excel('data/小木虫论坛-论文投稿-仅投稿求助(含描述）-20220810采集.xlsx')
    raw_data = raw_data[['标题', 'desc']]
    logger.info('xmc原数据条数：{}'.format(len(raw_data)))
    raw_data['标题'] = raw_data['标题'].apply(lambda x: clean_sentence(x))
    raw_data['desc'] = raw_data['desc'].apply(lambda x: clean_sentence(x))
    dropidx = raw_data[
        raw_data['标题'].str.cat(raw_data['desc'], sep='').str.contains(pat='|'.join(beacon), regex=True)].index
    raw_data.drop(dropidx, inplace=True)
    raw_data.dropna(axis=0, how='any', inplace=True)  # 删除有空值的行
    logger.info('xmc清洗后数据条数：{}'.format(len(raw_data)))
    raw_data.columns = ['title', 'desc']
    raw_data.to_csv('data/xmc.tsv', sep='\t')
    raw_data.to_excel('data/xmc.xlsx')


def clean_dxy_foreign():  # 清洗丁香园外文杂志投稿提问文本
    beacon = ['欢迎', '点赞', '祈福', '祝福', '散金', '撒花', '庆祝', '活动参与', '征稿']  # dxy
    raw_data = pd.read_excel('data/丁香园论坛-英文期刊投稿交流20220809采集（标题+详情）.xlsx')
    raw_data = raw_data[['标题', '正文']]
    raw_data['标题'] = raw_data['标题'].apply(lambda x: clean_sentence(x))
    raw_data['正文'] = raw_data['正文'].apply(lambda x: clean_sentence(x))
    logger.info('dxy原数据条数：{}'.format(len(raw_data)))
    # 删除含有无效数据特征词的行 #['标题', '正文']
    dropidx = raw_data[
        raw_data['标题'].str.cat(raw_data['正文'], sep='').str.contains(pat='|'.join(beacon), regex=True)].index
    raw_data.drop(dropidx, inplace=True)  # regex=True则pat是一个正则表达式，regex=False表示pat是一个字符串
    logger.info('dxy清晰后数据条数：{}'.format(len(raw_data)))
    # 统计“正文”为空的提问文本数量
    cnt = 0
    for i in raw_data.itertuples():
        if i[2] != 'nan':
            cnt += 1
    logger.info('含描述文本的提问数：{}'.format(cnt))
    # 使用标题文本对空的“正文”进行填充
    raw_data = raw_data.values.tolist()
    for idx, i in enumerate(raw_data):
        if i[1] == 'nan':
            raw_data[idx][1] = ' '  # i[0]
    pd.DataFrame(raw_data, columns=['title', 'desc']).to_csv('data/dxy_foreign.tsv', sep='\t', index=False)


def clean_dxy_cn():  # 清洗丁香园中文杂志投稿提问文本
    beacon = ['欢迎', '点赞', '祈福', '祝福', '散金', '撒花', '庆祝', '活动参与', '征稿']  # dxy
    raw_data = pd.read_excel('data/丁香园论坛-中文期刊投稿交流20220810采集（标题+详情）.xlsx')
    raw_data = raw_data[['标题', '正文']]

    raw_data['标题'] = raw_data['标题'].apply(lambda x: clean_sentence(x))
    raw_data['正文'] = raw_data['正文'].apply(lambda x: clean_sentence(x))

    logger.info('dxy原数据条数：{}'.format(len(raw_data)))
    dropidx = raw_data[
        raw_data['标题'].str.cat(raw_data['正文'], sep='').str.contains(pat='|'.join(beacon), regex=True)].index
    raw_data.drop(dropidx, inplace=True)
    logger.info('dxy清晰后数据条数：{}'.format(len(raw_data)))
    # 统计“正文”为空的提问文本数量
    cnt = 0
    for i in raw_data.itertuples():
        if i[2] == 'nan':
            cnt += 1
    logger.info('不含描述文本的提问数：{}'.format(cnt))
    # # 使用标题文本对空的“正文”进行填充
    # raw_data = raw_data.values.tolist()
    # for idx, i in enumerate(raw_data):
    #     if i[1] == 'nan':
    #         raw_data[idx][1] = i[0]
    raw_data.columns = ['title', 'desc']
    pd.DataFrame(raw_data).to_csv('data/dxy_cn.tsv', sep='\t')
    pd.DataFrame(raw_data).to_excel('data/dxy_cn.xlsx')


if __name__ == '__main__':
    # clean_xmc()
    # clean_dxy_foreign()
    clean_dxy_cn()
