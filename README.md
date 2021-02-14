## Pyminer: A Python CLI for Mining Scientific Literature. ⛏ 💻

### Prerequisites:
- Python 3.8
- Nodejs >=14.0

### Quickstart:
```
pip install journal-miner==1.0
```
### Usage:
```
Usage: pyminer [OPTIONS] QUERY

  Arguments:

  QUERY The main search string.

Options:
  -l, --limit INTEGER   Number of papers to mine. Default = 1000
  -kw, --keywords LIST  Keywords to mine.
  --help                Show this message and exit.
```
e.g.
```
pyminer polymerase -kw ['inhibitor', 'rna', 'promoter'] -l 100
```
### Output:
A .csv will be created in the current working directory storing paper  \n
with: Date, Title, Score, Keywords. Papers will ranked by their \n
score which is the sum of keyword appearances in the main text.
