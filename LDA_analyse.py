#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/8/3 17:13 
# @Description:基于LDA的用户提问主题分析
import numpy as np
import gensim
import pandas as pd
import jieba
import string
import matplotlib.pyplot as plt
import matplotlib
from collections import Counter
from gensim import corpora
from ltp import LTP
from zhon.hanzi import punctuation

punctuations = string.punctuation + punctuation
stopwords = [str(i).strip('\n') for i in open('stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
stopwords += [i for i in punctuations]  # 将标点加入停用词
ltp = LTP()


def compute_lda(doc, max_topic_num, cluster_id=0):
    '''
    :param doc:列表，每个元素是文本（句子）
    :return:
    '''
    doc = [jieba.lcut(str(i)) for i in doc]
    for idx, i in enumerate(doc):
        doc[idx] = [word for word in i if word not in stopwords]

    dictionary = corpora.Dictionary(doc)  # 创建语料的词语词典，每个单独的词语都会被赋予一个索引
    doc_term_matrix = [dictionary.doc2bow(d) for d in doc]  # 使用上面的词典，将转换文档列表（语料）变成 DT 矩阵
    Lda = gensim.models.ldamodel.LdaModel  # 使用gensim创建LDA模型实例
    perplexity = []
    best_topic_num = 0
    for i in range(1, max_topic_num, 5):
        ldamodel = Lda(doc_term_matrix, num_topics=i, id2word=dictionary, passes=50)  # 在DT矩阵上运行和训练LDA模型
        perplex = ldamodel.log_perplexity(doc_term_matrix)
        perplexity.append(perplex)
        if perplex == np.max(np.array(perplexity)):
            best_topic_num = i
    best_lda = Lda(doc_term_matrix, num_topics=best_topic_num, id2word=dictionary, passes=50)
    pd.DataFrame(best_lda.print_topics(num_topics=10, num_words=10)).to_excel(
        'clustered_out/LDAcluster_{}.xlsx'.format(cluster_id))
    # 绘制困惑度折线图
    plt.plot(range(1, max_topic_num, 5), perplexity, 'o')
    # plt.scatter(range(1, max_topic_num, 5), perplexity)
    plt.xlabel('主题数')
    plt.ylabel('困惑度')
    plt.rcParams['font.sans-serif'] = ['SimHei']
    # matplotlib.rcParams['axes.unicode_minus'] = False
    plt.legend(loc='best')
    plt.show()
    plt.savefig('clustered_out/LDAperplex_{}.jpg'.format(cluster_id))


if __name__ == '__main__':
    data = pd.read_excel('clustered_out/bert-kmeans-clustered_xmc.xlsx', index_col=[0])
    for i in data.groupby(['cluster_id']):
        cluster_id = i[0]
        doc = i[1]['text'].values.tolist()
        ldamodel = compute_lda(doc, max_topic_num=20, cluster_id=cluster_id)
