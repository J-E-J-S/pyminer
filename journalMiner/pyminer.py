#!/usr/bin/env python

import sys
import os
from bs4 import BeautifulSoup
import pandas as pd
import shutil
import click
import subprocess

def get_papers(query, folder_path, limit):

    base = 'cmd /c getpapers -q ' # base of getpapers request
    query = ('{}' + query + '{}').format('"', '"') # formatting search string for wrapper
    output_dir = ('{}' + folder_path).format(' -o ') # spacing and option
    limit = ('{}' + str(limit)).format(' -k ')

    command = base + query + output_dir + limit + ' -x'

    # Try to see if getpapers is installed
    try:
        subprocess.run(command, check = True)
    except subprocess.CalledProcessError:
        print('getpapers not found, begining install with npm.')
        os.system('npm install -g getpapers')
        os.system(command)
        print('getpapers installed.')

    return

def extract_xml(xml_path, keywords):
    # Extracts Key Article Data from Paper XML

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
    keyword_hits = {}
    content = soup.text.lower()
    for word in keywords:
        frequency = content.count(word.lower())
        keyword_hits[word] = frequency

    score = sum(keyword_hits.values()) # Calculate overall score for paper

    return date, title, score, keyword_hits

def iterate_folder(folder_path, keywords):

    df = pd.DataFrame(columns=['Date', 'Title', 'Score']) # Init dataframe

    # Iterate through getpapers generated output dir
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            path = os.path.join(root, file)
            if path.endswith('.xml'):
                date, title, score, keyword_hits = extract_xml(path, keywords)
                entry = {'Date':date, 'Title':title, 'Score':score}
                # Create new column for each keyword searched
                for word in keyword_hits:
                    entry[word] = keyword_hits[word]

                df = df.append(entry, ignore_index=True) # Add paper data to dataframe

    # Order df so highest score first
    df = df.sort_values(by='Score', ascending=False)

    return df

def export_mine(df, query, folder_path):
    # Exports mine as .csv and deletes the local mine resources

    # Export df to .csv (Excel)
    query = query.replace(' ', '_') # Format for multi-word query strings
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

def _getVersion(ctx,param, value):

    if not value or ctx.resilient_parsing:
        return

    folder = os.path.abspath(os.path.dirname(__file__))
    init = os.path.join(folder, '__init__.py')
    f = open(init, 'r')
    version = f.read()
    version = version.replace('__version__ = ', '')
    version = version.replace('\'', '')
    version = version.replace('\n', '' )
    f.close()
    click.echo(version)
    ctx.exit()

@click.command()
@click.argument('query')
@click.option('-l', '--limit', default = 1000, type=int, help='Number of papers to mine. Default = 1000' )
@click.option('-kw', '--keyword', multiple=True, help='Keyword to mine.')
@click.option('-v', '--version', is_flag=True, callback=_getVersion, expose_value=False, is_eager=False, help='Show version number and exit.')
def cli(query, keyword, limit):

    """Arguments:\n
    QUERY The main search string.
    """

    # Make sure not overwriting existing folder
    path_query = query.replace(' ', '_') # Format for multi-word query strings
    folder_path = os.path.join(os.getcwd(), path_query + '_mine')
    count = 1
    while os.path.exists(folder_path):
        folder_path = os.path.join(os.getcwd(),str(count) + '_' +  path_query + '_mine')
        count += 1

    get_papers(query, folder_path, limit)

    # If not keywords added, then query used as keyword
    if len(keyword) == 0:
        keyword = (query,)

    output_path = export_mine(iterate_folder(folder_path, keyword), query, folder_path)

    click.echo('Mining Complete.')
    click.echo('Results available at: ' + output_path )
    return

if __name__ == '__main__':
    cli()
