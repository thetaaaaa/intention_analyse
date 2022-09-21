#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/9/3 21:53 
# @Description: 对xmc数据进行预标注

import pandas as pd
import re

xmc = pd.read_excel('data/xmc.xlsx', index_col=[0])
tags = ['期刊推荐', '期刊属性', '行业术语',
        '审稿意见解读与回应', '投稿流程和手续的咨询与建议', '稿件状态研判', '价值判断', '写作建议',
        '情感认同', '低价值问题']
tags = {tag: 1 for tag in tags}
xmc = pd.concat([xmc, pd.DataFrame(columns=tags.keys())])
for row in xmc.itertuples():
    title_desc = str(row.title) + str(row.desc)
    if re.findall('寻求|推荐', title_desc):
        xmc.loc[row.Index, '期刊推荐'] = tags['期刊推荐']
    elif re.findall('会被拒', title_desc):
        xmc.loc[row.Index, '稿件状态研判'] = tags['稿件状态研判']

xmc.to_excel('data/xmc_tagging.xlsx')
