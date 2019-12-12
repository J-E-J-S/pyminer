# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
from nltk.corpus import stopwords as stopwords
import nltk.tokenize as tokenize
import os

# %%
file_path = r"C:\Users\James\Documents\george_test\PMC3836802\fulltext.xml"
folder_path = r"C:\Users\James\Documents\george_test"
#search_list = ['FAD', 'FMN', 'LOV', 'Cysteine', 'transcription', 'factor', 'blue'] 

def read_folder(folder_path):
    dictionary_of_common_words = {}
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            file_path = r'{}\{}'.format(folder_path, file)
            f=open(file_path,'r')
            dictionary_of_common_words[file] = filter_xml(f)
            f.close()
            
read_folder(folder_path)

# %%
            
def filter_xml(f):
    '''takes in xml file path and outputs list of most common words'''
    soup = BeautifulSoup(f, 'lxml')
    text = soup.text
    custom_list = ['']
    stop_words = list(stopwords.words('english')) + custom_list
    list_of_words = text.split(' ')
#    word_tokens = tokenize(text) 
    filtered_text = []
    key_words = {}
    for i in list_of_words: 
        if i not in stop_words:
            filtered_text.append(i)
    for i in filtered_text: 
        key_words[i] = key_words.get(i,0) + 1
    most_common_words = sorted(key_words, key=key_words.get, reverse= True)
    return most_common_words

    
# %%
nltk.download('stopwords')