####
# -*- coding: utf-8 -*-
# Created on Sun Dec 29 17:56:58 2019
# @author: James Sanders and George Pearse
###

import sys
import os
from bs4 import BeautifulSoup
from nltk.corpus import stopwords as stopwords
import nltk.tokenize as tokenize
import nltk
import pandas as pd

search_string = 'Type Primary Keyword Here'
folder_path = r"C:\Type Output Dir Path Here" 

search_list = ['string_1', 'string_2', 'string_n']

def get_papers(search_string, folder_path, limit):
    ''' python wrapper for getpapers command, creates file system'''
    base = 'cmd /k getpapers -q ' # base of getpapers request
    search_string = ('{}' + search_string + '{}').format('"', '"') # formatting search string for wrapper
    output_dir = ('{}' + folder_path).format(' -o ') # spacing and option
    limit = ('{}' + str(limit)).format(' -k ')

    command = base + search_string + output_dir + limit + ' -x'

    os.system(command)

    return

def extract_data(file_path):
    '''takes in xml file path and outputs list of most common words'''
    f = open(file_path, 'r')
    soup = BeautifulSoup(f, 'html.parser') # Beautiful soup takes the code written to format some piece of text and turns it into nested objects you can navigate
    f.close()
    text = soup.text # This is extracting just the written text and removing the pieces of code that purely exist for formatting
    title = soup.find('article-title').text # extracts the title to act as first column of DataFrame
    date = ''
    try:
        day,month,year = soup.find('day'),soup.find('month'),soup.find('year')
        date = year.text + '-' + month.text + '-' + day.text
    except:
        pass
     # Can also edit this (add more words) -> other words that you don't want to count (words that aren't included in stopwords)
    list_of_words = text.split(' ') # converting the body of text into a list of distinct word
    key_words = {} # initialising the dictionary to act as a counter
    for i in list_of_words:
        if i in search_list: # making sure that common words such as 'a', 'the' etc. do not come up in the counter, because they would definitely be the most common
            key_words[i] = key_words.get(i,0) + 1 # removing stop words from the text by adding only those that are not in stop words
    score = sum(key_words.values())
    return date, title, score, key_words


def read_folder(folder_path):
    ''' Apply to DataFrame -> need to make a DataFrame of file_paths first '''
    filepaths = []
    for subdir, dirs, files in os.walk(folder_path):
        for file in files:
            if file[-3:] == 'xml': # making sure you only open the actual article as opposed to the other files in the folder
                file_path = r'{}\{}'.format(subdir, file)
                filepaths.append(file_path)
    df_filepaths = pd.DataFrame(filepaths)
    df_filepaths['Date'], df_filepaths['Title'],df_filepaths['Score'], df_filepaths['Keywords'] = zip(*df_filepaths[0].apply(lambda x: extract_data(x)))
    df_filepaths.index = range(0,len(df_filepaths))
    df_filepaths = df_filepaths[['Date','Title','Score','Keywords']]
    df_filepaths.to_csv(folder_path + '\\results.csv')
    return df_filepaths

def main():
    get_papers(search_string, folder_path, limit)
    read_folder(folder_path)

if __name__ == '__main__':
    main()
