#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/9/5 19:35 
# @Description:构造意图识别数据集


import pandas as pd
from sklearn.utils import shuffle
from tqdm import tqdm

data = pd.read_excel('data/xmc_taged0921.xlsx', index_col=[0])
corpus = []
for row in tqdm(data.itertuples()):
    for attr in data.columns[2:]:
        if getattr(row, attr) == 1:
            corpus.append([row.title, row.desc, attr])

corpus = corpus[:5500]

cut_idx = len(corpus) // 10

corpus = pd.DataFrame(corpus, columns=['title', 'desc', 'label'])
corpus.dropna(axis=0, how='any', inplace=True)
# 类别归并优化:
# 合并投稿系统使用问题、投稿策略、行业术语、价值判断、投稿流程和手续的咨询与建议为投稿方式
# 合并情绪输出或不表达信息需求、稿件状态研判为稿件状态研判
corpus.replace({'label':{'投稿系统使用问题':'投稿方式','投稿策略':'投稿方式','投稿流程和手续的咨询与建议':'投稿方式'}},inplace=True)
corpus.replace({'label':{"情绪输出或不表达信息需求":"稿件状态研判"}},inplace=True)
corpus.to_csv('xmc/title_desc.tsv', sep='\t', index=0)
corpus = shuffle(corpus, random_state=2023)

# 划分训练、测试集
train_corpus = corpus[cut_idx:]
test_corpus = corpus[:cut_idx]
# 标题数据集
title_train, title_test = train_corpus[['label', 'title']], test_corpus[['label', 'title']]
title_train.to_csv('xmc/title/train.tsv', sep='\t', index=0, header=['label', 'title'])
title_test.to_csv('xmc/title/test.tsv', sep='\t', index=0, header=['label', 'title'])
# 描述文本数据集
desc_train, desc_test = train_corpus[['label', 'desc']], test_corpus[['label', 'desc']]
desc_train.to_csv('xmc/desc/train.tsv', sep='\t', index=0) #, header=None
desc_test.to_csv('xmc/desc/test.tsv', sep='\t', index=0, ) # header=None
# 标题——描述文本数据集
tile_desc_train, tile_desc_test = train_corpus[['label', 'title', 'desc']], test_corpus[['label', 'title', 'desc']]
tile_desc_train.to_csv('xmc/title_desc/train.tsv', sep='\t', index=0) # , header=None
tile_desc_test.to_csv('xmc/title_desc/test.tsv', sep='\t', index=0) # , header=None


'''构造预训练数据集'''
# 基于描述文本的预训练数据集
desc4pttrain, desc4pttest = train_corpus[['desc']], test_corpus[['desc']]
desc4pttrain.to_csv('xmc4pt/train.txt', sep='\t', index=0, header=None)
desc4pttest.to_csv('xmc4pt/test.txt', sep='\t', index=0, header=None)