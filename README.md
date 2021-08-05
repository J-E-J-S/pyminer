## Pyminer: A Python CLI for Mining Scientific Literature. 🔬⛏

![](/assets/pyminer.gif)

### Prerequisites:
- Python >=3.8
- Nodejs >=14.0

### Quickstart:
```
pip install journal-miner
```
### Usage:
```
Usage: pyminer [OPTIONS] QUERY

  Arguments:

  QUERY The main search string.

Options:
  -l, --limit INTEGER   Number of papers to mine. Default = 1000
  -kw, --keywords LIST  Keyword to mine.
  --help                Show this message and exit.
```
e.g.
```
pyminer 'RNA polymerase III' -kw inhibitor -kw 'TATA box' -kw enzyme -l 100
```
### Output:
A .csv will be created in the current working directory storing paper  
with: Date, Title, Score, Keywords. Papers will ranked by their  
score which is the sum of keyword appearances in the main text.
