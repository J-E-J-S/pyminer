# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from bs4 import BeautifulSoup
from nltk.corpus import stopwords as stopwords
import nltk.tokenize as tokenize
import os
import nltk
import pandas as pd

# %%

folder_path = r"C:\Users\James\Documents\george_test"

# %% Main Tools

def get_frequency(file_path):
    '''takes in xml file path and outputs list of most common words'''
    f = open(file_path, 'r')
    soup = BeautifulSoup(f, 'lxml')
    text = soup.text
    custom_list = ['']
    stop_words = list(stopwords.words('english')) + custom_list
    list_of_words = text.split(' ')
    filtered_text = []
    key_words = {}
    for i in list_of_words: 
        if i not in stop_words:
            filtered_text.append(i)
    for i in filtered_text: 
        key_words[i] = key_words.get(i,0) + 1
    return key_words

def get_most_common_words(key_words):
    '''sorts the list of most common words'''
    most_common_words = sorted(key_words, key=key_words.get, reverse= True)
    return most_common_words
    
def get_frequency_sorted(most_common_words,key_words):
    '''uses the dictionary created earlier to get the frequency of the most_common_words'''
    words_frequency = []
    for i in most_common_words: 
        words_frequency.append((i, key_words[i]))
    return words_frequency

def get_matched(search_list, words_frequency):
    '''compares search dictionary'''
    matched = []
    # trying to compare tuple to single value
    for word_frequency in words_frequency:
        if word_frequency[0] in search_list:
            matched.append(word_frequency)
    return matched

# %% Combining all of the tools 

def do_everything(file_path, search_list):
    key_words = get_frequency(file_path)
    most_common_words = get_most_common_words(key_words)
    frequency = get_frequency_sorted(most_common_words,key_words)
    matched = get_matched(search_list,frequency)
    score = 0
    for match in matched:
        score = score + match[1]
    return (score, matched)


# %% Batch Management
    
def read_folder(folder_path, search_list):
    ''' -> can't handle the file that isn't html'''
    results = {}
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file[-3:] == 'xml':
                file_path = r'{}\{}'.format(subdir, file)
                results[str(subdir)] = do_everything(file_path, search_list)
                f.close()
    results_df = pd.DataFrame(results)
    return results_df

search_list = ['FAD', 'FMN', 'LOV', 'Cysteine', 'transcription', 'factor', 'blue']             
folder_path = r"C:\Users\James\Documents\george_test"
results_df = read_folder(folder_path, search_list)

resultsTRANPOSE = results_df.T
sorted_df = resultsTRANPOSE.sort_values(by=[0],ascending=False)


# %%
nltk.download('stopwords')