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
#    string = str_replace_re(string, r"http\S+") # remove http link in string
#    string = str_replace_re(string, "\u200b") # remove zero width space
#    string = str_replace_re(string, "\xa0")
#    string = str_replace_re(string, "APP下载地址：")
#    string = str_replace_re(string, "\', \'")
    string = string.replace("\u200b","") # remove zero width space
    string = re.sub(r"http\S+", "", string) # remove http link in string
    string = string.replace("\xa0","") # remove zero width space
    string = string.replace("APP下载地址：","") 
    string = string.replace("\', \'"," ") 
    string = string.replace("↓↓↓"," ") 
    string = string.replace("\u3000"," ") 
    
    for char in filtered_chars:
        string = str_replace(string, char)

    for char in split_chars:
        string = str_replace(string, char, split_mark)

    # Remove consecutive split marks
    while split_mark + split_mark in string:
        string = str_replace(string, split_mark + split_mark, split_mark)

    return string

def preprocess_file(inFile):
    
    #inFile = "D:/NLP/tonghuashun-short.txt"
    input_file = open(inFile, "r", encoding='utf8')  # Open input file
    output_file_name = inFile.split('.')[0] + "-preprocessed.txt"
    output_file = open(output_file_name, "w", encoding='utf8')

    string = input_file.read()
    output_file.write(preprocessing(string))
    
    return output_file_name
