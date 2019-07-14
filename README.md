# Machine Learning: Commits

Predicting the main programming language of actual repositories on GitHub purely based on the contents of the commit messages using supervised text learning.

## Install:
1. Install Python3
2. Clone repository
3. Install requirements, run the following command within the project directory and install any packages that might still be missing:
```python3 -m pip install -r requirements.txt```

## Run:

### Alternative 1: Use crawled data
1.  Download dataset from https://github.com/kvnmlr/ml-commits/blob/files/files.zip and extract in folder project root.
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

## Results:
In 2 seconds:
```
Correct: 166
Wrong: 132
Languages considered: 25
Classifier Score: 55.70%
```
