# -*- coding: utf-8 -*-
"""
Master file for creating dictionary and parsing Chinese text

Created on Sat Sep 30 10:34:01 2017

@author: Frank-Mia
"""
import importlib
import pre
import dict_creat
import word_split
importlib.reload(dict_creat)
#importlib.reload(word_split)
import word_count

# input file
fileIn = "D:/NLP/tonghuashun-20170929-2-preprocessed.txt"

# preprosess
fileProcessed = pre.preprocess_file(fileIn)

# create dictionary
fileDict = dict_creat.build_dictionary(fileProcessed)

# word split
fileSplit = word_split.word_split(fileProcessed, fileDict)

# word count
word_count.word_count(fileSplit)
