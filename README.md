# Machine Learning: Commits

Just trying to learn patterns in commit messages that can be linked to programming languages.

## Install:
1. Install Python3
2. Clone repository
3. Install requirements, run the following command within the project directory:
```python3 -m pip install -r requirements.txt```

## Run:

### Alternative 1: Use crawled data
1.  Download dataset from ... and save in folder ml-commits/files
2.  Run classification:
```python3 classification/classify.py```

### Alternative 2: Crawl yourself:
1. Enter your GitHub username and password in the credentials.json file
2. Run the crawler:
```python3 crawler.py```
3. Extract languages and commit message:
```python3 features_extractor.py```
4. Run classification:
```python3 classification/classify.py```
