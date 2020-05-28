GeorgesMarvelousMiner
======================

This tool allows mining of scientific papers through a 2-part search. 

1. A primary keyword is used to scrape all relevent papers from open-access databases 
	* Performed with the [getpapers](https://github.com/ContentMine/getpapers) from [ContentMine](http://contentmine.org/)

2. A list of secondary keywords to identify relevant papers within this mine 
	* Script generates a results.csv file which can be filtered for the most relevant papers 

Manual
-------

**Pre-Requisites:** Follow links for install instructions 
* [Python 3](https://www.python.org/download/releases/3.0/)
* [Pip](https://pip.pypa.io/en/stable/installing/)
* [getpapers](https://github.com/ContentMine/getpapers)   
* Python packages 
	* bs4
	* nltk 
	* pandas 

**Note:**  
* Can install python packages through pip in terminal either via 'pip install package_name' or 'python -m pip install package_name'
	* install command may vary depending on using Windows or macOS
* e.g. python -m pip install bs4 

**Instructions:**

 1. Define the primary keyword by typing within the '' on line 9: 
 ```
 search_string = 'Type Primary Keyword Here'
 ```
 2. Define the desired output directory (this will be created if not already made), on line 10
 	* Note - path has to be in the C:\dira\dirb\etc form not \c\dira\dirb\etc
 ```
folder_path = r"C:\Type Path Here"
```
3. Set how many papers you want to search through, on line 11
	* Default set to 1000 papers, note a file system will be created for each of these papers so it is better to start with a defined quantity
```
limit = 1000 
```
4. Define the list of secondary keywords as a list of strings on line 13
```
search_list = ['string_1', 'string_2', 'string_n']
```
5. Run the script from your IDE or save and run from terminal as
```
python JournalMiner.py 
```

The script will then proceed to gather all xml files for the paper and generate a 'results.csv' file with a breakdown of all the papers by title, year published, and a total relevance score and how many times each individual secondary keyword appeared in that paper. 

Find the papers most relevant to you and analyse them further manually. 






To-Do:
------ 
* Increase the speed of data extraction / simplify code
* Connect directly to the online database
* Replace iteration through folder and use .apply

