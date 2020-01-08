# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 17:56:58 2019

@author: James Sanders and George Pearse
"""

# %% Debugging / finding modules / extending os path 

import sys 
import os 

print(sys.path) 
sys.path.append(r"C:\\Users\\GeorgePearse\\Anaconda3\\Lib\\site-packages")
# %%

from bs4 import BeautifulSoup
from nltk.corpus import stopwords as stopwords
import nltk.tokenize as tokenize
import os
import nltk
import pandas as pd

# %%
def send_title(title):
    return title

def get_frequency(file_path):
    '''takes in xml file path and outputs list of most common words'''
    f = open(file_path, 'r')
    soup = BeautifulSoup(f, 'html.parser') # Beautiful soup takes the code written to format some piece of text and turns it into nested objects you can navigate
    f.close()
    text = soup.text # This is extracting just the written text and removing the pieces of code that purely exist for formatting
    title = soup.find('article-title').text # extracts the title to act as first column of DataFrame 
    send_title(title) 
    custom_list = ['The'] # Can also edit this (add more words) -> other words that you don't want to count (words that aren't included in stopwords)
    stop_words = list(stopwords.words('english')) + custom_list
    list_of_words = text.split(' ') # converting the body of text into a list of distinct words
    filtered_text = []
    key_words = {} # initialising the dictionary to act as a counter
    for i in list_of_words:
        if i not in stop_words: # making sure that common words such as 'a', 'the' etc. do not come up in the counter, because they would definitely be the most common
            filtered_text.append(i) # removing stop words from the text by adding only those that are not in stop words
    for i in filtered_text:
        key_words[i] = key_words.get(i,0) + 1 # counter to find the number of times that any words occur
    return key_words, title


def get_most_common_words(key_words):
    '''sorts the list of most common words'''
    most_common_words = sorted(key_words, key=key_words.get, reverse= True) # ordering words by how often they occur
    return most_common_words

def get_frequency_sorted(most_common_words,key_words):
    '''uses the dictionary created earlier to get the frequency of the most_common_words'''
    words_frequency = []
    for i in most_common_words:
        words_frequency.append((i, key_words[i])) #appending tuples of a word and its frequency
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
    '''just combining lots of the earlier functions'''
    key_words, title = get_frequency(file_path)
    most_common_words = get_most_common_words(key_words)
    frequency = get_frequency_sorted(most_common_words,key_words)
    matched = get_matched(search_list,frequency)
    score = 0
    for match in matched:
        score = score + match[1] # scoring an article based on how strongly it matches the your selected keywords
    return (title, score, matched)


# %% Batch Management

def read_folder(folder_path, search_list):
    ''' -> can't handle the file that isn't html'''
    results = {}
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file[-3:] == 'xml': # making sure you only open the actual article as opposed to the other files in the folder
                file_path = r'{}\{}'.format(subdir, file)
                results[str(subdir)] = do_everything(file_path, search_list) # creates a dictionary where the key is the name of the subfolder which contains the article -> should be replaced with the title of the article
    results_df = pd.DataFrame(results) # create a DataFrame (table) of the results
    resultsTRANPOSE = results_df.T # transposing the DataFrame so that it is more easily read
    sorted_df = resultsTRANPOSE.sort_values(by=[0],ascending=False)
    sorted_df.columns = ['Article Title','Score','Keywords']
    return sorted_df

# %%

search_list = ['FAD', 'FMN', 'LOV', 'Cysteine', 'transcription', 'factor', 'blue']
folder_path = r"C:\Users\GeorgePearse\projects\James\GeorgesMarvelousMiner\Test_1"

results = read_folder(folder_path,search_list) # this combines all the earlier pieces of code into one command
