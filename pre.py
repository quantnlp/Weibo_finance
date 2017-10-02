"""
Author: Yu Lou
"""
import re

def str_replace(string, str_from, str_to=""):
    """
    Replace str_from with str_to in string.
    """
    return str_to.join(string.split(str_from))


def str_replace_re(string, str_from, str_to=" "):
    """
    Replace str_from with str_to in string.
    str_from can be an re-expression.
    """
    return re.sub(str_from, str_to, string)

def preprocessing(string):
    """
    Preprocess string.
    :return: processed string
    """
    split_mark = "#"  # Split mark for output
    filtered_chars = ""  # Characters to ignore
    split_chars = " …《》，、。？！；：“”‘’'\n\r-=—()（）.【】『』［］[]〔〕"  # Characters representing split mark
    replace_chars = ["\u200b", "\xa0全文""\xa0", "↓↓↓", "\', \'", "\u3000", # special charactors
                     "发表了博文", "APP下载地址：",
                     "该微博因被多人举报，根据《微博社区管理规定》，已被删除。查看帮助：",
                     "抱歉，此微博已被作者删除。查看帮助：",
                     "抱歉，由于作者设置，你暂时没有这条微博的查看权限哦。查看帮助：",
                     "发布了头条文章：", "我发表了文章 "
            ]
#    string = string.replace("\u200b","") # remove zero width space
    string = re.sub(r"http\S+", "", string) # remove http link in string
    for ichar in replace_chars:
        string = string.replace(ichar,"")
#    string = string.replace("\xa0","") # remove zero width space
#    string = string.replace("APP下载地址：","") 
#    string = string.replace("\', \'"," ") 
#    string = string.replace("↓↓↓"," ") 
#    string = string.replace("\u3000"," ")
#    string = string.replace("该微博因被多人举报，根据《微博社区管理规定》，已被删除。查看帮助："," ") 
    
    for char in filtered_chars:
        string = str_replace(string, char)

    for char in split_chars:
        string = str_replace(string, char, split_mark)

    # Remove consecutive split marks
    while split_mark + split_mark in string:
        string = str_replace(string, split_mark + split_mark, split_mark)

    return string

def preprocess_file(fileIn):
    
    #inFile = "D:/NLP/tonghuashun-short.txt"
    input_file = open(fileIn, "r", encoding='utf8')  # Open input file
    output_file_name = "D:/NLP/data/dict/" + fileIn.split('.')[0].split("/")[-1] + "-processed.txt"
    output_file = open(output_file_name, "w", encoding='utf8')

    string = input_file.read()
    output_file.write(preprocessing(string))
    
    return output_file_name
