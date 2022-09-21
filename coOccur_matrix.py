#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/8/16 14:42 
# @Description:制作词共现矩阵。参考链接：https://blog.csdn.net/qklwdd6/article/details/79148582

import numpy as np
import time
import os
import pandas as pd
import string
from zhon.hanzi import punctuation
import logging

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(name)s -   %(message)s',
                    datefmt='%m/%d/%Y %H:%M:%S',
                    level=logging.INFO,
                    filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)

punctuations = string.punctuation + punctuation
baidu_stopwords = [str(i).strip('\n') for i in open('stopwords/baidu_stopwords.txt', 'r', encoding='utf-8').readlines()]
cn_stopwords = [str(i).strip('\n') for i in open('stopwords/cn_stopwords.txt', 'r', encoding='utf-8').readlines()]
scu_stopwords = [str(i).strip('\n') for i in open('stopwords/scu_stopwords.txt', 'r', encoding='utf-8').readlines()]
hit_stopwords = [str(i).strip('\n') for i in open('stopwords/hit_stopwords.txt', 'r', encoding='utf-8').readlines()]
stopwords = baidu_stopwords + cn_stopwords + scu_stopwords + hit_stopwords + [i for i in punctuations]  # 将标点加入停用词
stopwords = list(set(stopwords))


def log(func):
    log_dir = os.path.join('log', os.path.basename(__file__).split(".")[0])
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = logging.FileHandler((log_dir + os.sep + func.__name__ + '.log'), encoding='utf-8')
    logger.addHandler(handler)

    def wrapper(*args, **kwargs):
        print('%s %s called' % (str(time.strftime('%Y-%m-%d %X', time.localtime())), func.__name__))
        # print('Function:%s' % func.__doc__)
        return func(*args, **kwargs)

    return wrapper


def get_keywords(dic, threshold=1):
    '''选取频数大于等于Threshold的关键词构建一个集合，用于作为共现矩阵的首行和首列'''
    valid_words = {k: v for k, v in dic.items() if (str(k) not in punctuations) and (v >= threshold)}
    keywords_list = [a[0] for a in sorted(valid_words.items(), key=lambda x: x[1], reverse=True)]
    return keywords_list


def format_data(data, keywords):
    '''格式化需要计算的数据，将原始数据格式转换成二维数组'''
    formated_data = []
    for i in data:
        i = [word for word in i if (word in keywords) and (word not in punctuations)]  # 筛选出format_data中属于关键词集合的词
        i = list(set(filter(lambda x: x != '', i)))  # 去掉重复数据
        formated_data.append(i)
    return formated_data


def init_matirx(keywords):
    '''建立矩阵，矩阵的高度和宽度为关键词集合的长度 + 1'''
    edge = len(keywords) + 1
    # matrix = np.zeros((edge, edge), dtype=str)
    matrix = [['' for j in range(edge)] for i in range(edge)]
    # 初始化矩阵，将关键词集合赋值给第一列和第二列
    matrix[0][1:] = np.array(keywords)
    matrix = list(map(list, zip(*matrix)))
    matrix[0][1:] = np.array(keywords)
    return matrix


@log
def fill_matrix(matrix, formated_data):
    '''计算各个关键词共现次数'''
    keywords = matrix[0][1:]  # 列出所有关键词
    appeardict = {}  # 每个关键词与 [出现在的行(formated_data)的list] 组成的dictionary
    for w in keywords:
        appearlist = []
        i = 0
        for each_line in formated_data:
            if w in each_line:
                appearlist.append(i)
            i += 1
        appeardict[w] = appearlist
    for row in range(1, len(matrix)):
        # 遍历矩阵第一行，跳过下标为0的元素
        for col in range(1, len(matrix)):
            # 遍历矩阵第一列，跳过下标为0的元素
            # 实际上就是为了跳过matrix中下标为[0][0]的元素，因为[0][0]为空，不为关键词
            if col >= row:
                # 仅计算上半个矩阵
                if matrix[0][row] == matrix[col][0]:
                    # 如果取出的行关键词和取出的列关键词相同，则其对应的共现次数为0，即矩阵对角线为0
                    matrix[col][row] = str(0)
                else:
                    counter = len(set(appeardict[matrix[0][row]]) & set(appeardict[matrix[col][0]]))
                    matrix[col][row] = str(counter)
            else:
                matrix[col][row] = matrix[row][col]
    return matrix


if __name__ == '__main__':
    words_freq = dict(pd.read_excel('statistic/freq_xmc.xlsx', index_col=[0]).values.tolist())
    keywords = get_keywords(words_freq, 1000)
    seged_data = pd.read_excel('statistic/seged_xmc.xlsx', index_col=[0])
    seged_data['title'] = seged_data['title'].apply(lambda x: eval(x))
    seged_data['desc'] = seged_data['desc'].apply(lambda x: eval(x))
    data = pd.concat([seged_data['title'], seged_data['desc']]).values.tolist()
    formated_data = format_data(data, keywords)
    matrix = init_matirx(keywords)
    result_matrix = fill_matrix(matrix, formated_data)
    pd.DataFrame(result_matrix).to_csv('statistic/matrix_xmc.csv', index=False, header=False)
    # np.savetxt('statistic/matrix.txt', result_matrix, fmt=('%s,' * len(matrix))[:-1])
