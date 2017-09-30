# Weibo_finance
The best application of this repositary is: 
building a domain specific dictionary using all provided texts in one particular domain.

The amazing thing is that 
(1) it doesn't require labelled data;
(2) it doesn't require an explicit dictionary.

I applied this tool to parse financial tweets from Weibo. 
The word counts can be used as a reliable financial dictionary for parsing Chinese text using HanLP.

#####################
Only requires one input:
raw_text_to_be_analyzed.txt (encoding="utf8")

#####################
Important note: this tool is actually not good at parsing. It works best to build dictionary for other more advanced parsing systems.

#####################
Original code repositary from https://github.com/LouYu2015/analysis_on_the_story_of_a_stone
I automated different parts of code.
However, it is slow working with large text data.
I am optimizing it further.
