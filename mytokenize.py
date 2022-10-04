#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author:LinLitao
# @Time : 2022/10/4 11:39 
# @Description:
# import nltk
from nltk import word_tokenize

paragraph = "Theconnectinglinesinfig10andfig14isnotadded"
words = word_tokenize(paragraph)
print(words)
