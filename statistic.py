#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/8/15 20:19 
# @Description:多维度词频统计

import pandas as pd
from collections import Counter
from ltp import LTP
from zhon.hanzi import punctuation
import string
import pandas_profiling
import jieba.analyse
import random

punctuations = string.punctuation + punctuation
baidu_stopwords = [str(i).strip('\n') for i in open('stopwords/baidu_stopwords.txt', 'r', encoding='utf-8').readlines()]
cn_stopwords = [str(i).strip('\n') for i in open('stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
scu_stopwords = [str(i).strip('\n') for i in open('stopwords/scu_stopwords.txt', 'r', encoding='utf-8').readlines()]
hit_stopwords = [str(i).strip('\n') for i in open('stopwords/hit_stopwords.txt', 'r', encoding='utf-8').readlines()]
stopwords = baidu_stopwords + cn_stopwords + scu_stopwords + hit_stopwords + [i for i in punctuations]  # 将标点加入停用词
stopwords = list(set(stopwords))
ltp = LTP()


def word_seg(x):
    x = str(x)
    seg, hidden = ltp.seg([x])
    # pos = ltp.pos(hidden)
    # word_list = []
    # for i in zip(seg, pos):
    #     word_list += list(zip(i[0], i[1]))
    # return Counter(word_list).items()
    # sorted(Counter(wordlist).items(), key=lambda x: x[1], reverse=True)
    return seg[0]


def step1():  # 分词
    data = pd.read_csv('data/xmc.tsv', delimiter='\t', index_col=[0])[['title', 'desc']]
    data['title'] = data['title'].apply(lambda x: word_seg(x))
    data['desc'] = data['desc'].apply(lambda x: word_seg(x))
    data.to_excel('statistic/seged_xmc.xlsx')


def step2():  # 将所有的title和desc视为一个整体进行词频统计
    seged_data = pd.read_excel('statistic/seged_xmc.xlsx', index_col=[0])
    seged_data['title'] = seged_data['title'].apply(lambda x: eval(x))
    seged_data['desc'] = seged_data['desc'].apply(lambda x: eval(x))
    seged_data = seged_data.values.tolist()
    word_bag = []
    for title_desc in seged_data:
        title = title_desc[0]
        desc = title_desc[1]
        word_bag += [word for word in title + desc]
    word_bag = [word for word in word_bag if (word not in stopwords) and (word != '') and (word != ' ')]
    word_bag = sorted(Counter(word_bag).items(), key=lambda x: x[1], reverse=True)
    pd.DataFrame(word_bag).to_excel('statistic/freq_xmc.xlsx')


def auto_statistic():
    seged_data = pd.read_excel('statistic/seged_xmc-copy.xlsx')[['title', 'desc']]
    seged_data['title'] = seged_data['title'].apply(lambda x: len(eval(x)))
    seged_data['desc'] = seged_data['desc'].apply(lambda x: len(eval(x)))
    pfr = pandas_profiling.ProfileReport(seged_data)
    pfr.to_file('statistic/report_xmc.html')


def textrank_keywords():
    sent1 = '北京故宫是中国明清两代的皇家宫殿，旧称为紫禁城，位于北京中轴线的中心，是中国古代宫廷建筑之精华。'
    res1 = jieba.analyse.textrank(sent1, topK=10, withWeight=True,
                                  allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nrt', 'z', 'r', 'x'))
    for word, weight in res1:
        print('%s %s' % (word, weight))

    sent2 = '北京故宫是中国明清两代的皇家宫殿，旧称为紫禁城。前方是太和殿，是世界是最美的宫殿。'
    res2 = jieba.analyse.textrank(sent2, topK=10, withWeight=True,
                                  allowPOS=('ns', 'n', 'vn', 'v', 'nr', 'nrt', 'z', 'r', 'x'))
    for word, weight in res2:
        print('%s %s' % (word, weight))


if __name__ == '__main__':
    # auto_statistic()
    # textrank_keywords()
    data = pd.read_csv('data/xmc.tsv', delimiter='\t', index_col=[0]).values.tolist()
    random.shuffle(data)
    pd.DataFrame(data[:500]).to_csv('user_coding/random500xmc.tsv', sep='\t')
