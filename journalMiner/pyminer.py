#!/usr/bin/env python

import sys
import os
from bs4 import BeautifulSoup
import pandas as pd
import shutil
import click

def get_papers(query, folder_path, limit):

    base = 'cmd /c getpapers -q ' # base of getpapers request
    query = ('{}' + query + '{}').format('"', '"') # formatting search string for wrapper
    output_dir = ('{}' + folder_path).format(' -o ') # spacing and option
    limit = ('{}' + str(limit)).format(' -k ')

    command = base + query + output_dir + limit + ' -x'

    # Try to see if getpapers is installed
    try:
        os.system(command)
    except:
        os.system('npm install -g getpapers')
        os.system(command)

    return

def extract_xml(xml_path, keywords):

    ''' Extracts Key Article Data from Paper XML '''

    with open(xml_path, 'r') as f:
        soup = BeautifulSoup(f, 'html.parser')
        f.close()

    # Extract Title
    title = soup.find('article-title').text # Find xml element tag

    # Extract Date or return NaN if not found
    try:
        day, month, year = soup.find('day'), soup.find('month'), soup.find('year')
        date = year.text + '-' + month.text + '-' + day.text
    except:
        date = 'NaN'

    # Extract Key Word Counts and Paper Score
    content = soup.text.split(' ') # List of words in article without xml tags
    keyword_hits = {}
    for word in content:
        if word in keywords:
            keyword_hits[word] = keyword_hits.get(word, 0) + 1 # Dictionary Counter

    score = sum(keyword_hits.values()) # Calculate overall score for paper

    return date, title, score, keyword_hits

def iterate_folder(folder_path, keywords):

    df = pd.DataFrame(columns=['Date', 'Title', 'Score', 'KeyWords']) # Init dataframe

    # Iterate through getpapers generated output dir
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.xml'):
                date, title, score, keyword_hits = extract_xml(path, keywords)
                entry = {'Date':date, 'Title':title, 'Score':score, 'KeyWords':keyword_hits}
                df = df.append(entry, ignore_index=True) # Add paper data to dataframe

    # Order df so highest score first
    df = df.sort_values(by='Score', ascending=False)

    return df

def export_mine(df, query, folder_path):

    ''' Exports mine as .csv and deletes the local mine resources '''

    # Export df to .csv (Excel)
    entries = df['Title'].count()
    output_path = os.path.join(os.getcwd(), query + '_' + str(entries) + '.csv')

    # Changes output .csv name depending on if file already exists - allows repeated mines without deleting files
    count = 1
    while os.path.exists(output_path):
        output_path = os.path.join(os.getcwd(), str(count) + '_' + query + '_' + str(entries) + '.csv')
        count += 1

    df.to_csv(output_path, index=False)

    # Delete Mine
    shutil.rmtree(folder_path)

    return output_path

@click.command()
@click.argument('query')
@click.option('-l', '--limit', default = 1000, type=int, help='Number of papers to mine. Default = 1000' )
@click.option('-kw', '--keywords', multiple=True, help='Keyword to mine.')
def cli(query, keywords, limit):

    """Arguments:\n
    QUERY The main search string.
    """

    # Make sure not overwriting existing folder
    folder_path = os.path.join(os.getcwd(), query + '_mine')
    count = 1
    while os.path.exists(folder_path):
        folder_path = os.path.join(os.getcwd(),str(count) + '_' +  query + '_mine')
        count += 1

    get_papers(query, folder_path, limit)
    output_path = export_mine(iterate_folder(folder_path, keywords), query, folder_path)

    click.echo('Mining Complete.')
    click.echo('Results available at: ' + output_path )
    return

if __name__ == '__main__':
    cli()
