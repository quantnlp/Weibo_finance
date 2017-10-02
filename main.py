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
# importlib.reload(dict_creat)
# importlib.reload(word_split)
import word_count
import os
import glob
# input file
dirIn = "D:/NLP/data/"
os.chdir(dirIn)
filesTxt = glob.glob("*.txt")

for ifile in filesTxt[len(filesTxt)-1:len(filesTxt)-7:-1]:
#    fileIn = "D:/NLP/data/weibo_content-finance3-20170929-2735136620.txt"
    fileIn = ifile
    print("*" *20)
    print("Working on file " + fileIn)
    # preprosess
    fileProcessed = pre.preprocess_file(fileIn)
    
    # create dictionary
    fileSizeFactor = round(os.path.getsize(fileIn)/1000/100)
#    fileDict = dict_creat.build_dictionary(fileProcessed, fileSizeFactor)
    fileDictClass = dict_creat.Dict_create(fileProcessed, fileSizeFactor)
    fileDict = fileDictClass.build_dictionary()
    
    # word split
    fileSplit = word_split.word_split(fileProcessed, fileDict)
    
    # word count
    word_count.word_count(fileSplit)
