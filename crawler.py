import requests
import json
import time
import os
import atexit

api_limiter = (60 ** 2) / 5001.0  # max possible requests per hour allowed by Authenticated API
file_name = 'files/repos.json'
credentials_file = 'credentials.json'

access_token = 'b54f2b467f6b50145bee1b1c05b0395bf954db2f'
repos_crawled = 0
start_with = 185000000  # ensure we take new repos
t = time.time()


class CrawlerException(Exception):
    pass


def wait():
    global t
    sleep = api_limiter - (time.time() - t)
    print(sleep)
    print(wait)
    time.sleep(sleep)
    t = time.time()


def close_file():
    global repos_crawled
    print(f'Stopping crawler after {repos_crawled} repos')
    with open(file_name, 'a+') as file:
        file.write('\n]')


def make_request(url):
    r = requests.get(url, auth=basicAuthCredentials)
    if r.status_code > 400:
        raise CrawlerException('Query failed with message: ' + r.text)
    return json.loads(r.text)


def retrieve_repo(since):
    repo_list = make_request(f'https://api.github.com/repositories?since={since}')
    return repo_list


def retrieve_languages(name):
    language_list = make_request(f'https://api.github.com/repos/{name}/languages')
    return language_list


def retrieve_commits(name):
    commits_list = make_request(f'https://api.github.com/repos/{name}/commits')
    return list(map(lambda commit: commit['commit']['message'], commits_list))


def crawl_repos():
    global repos_crawled
    global basicAuthCredentials
    crawl_goal = 20000  # would run for 4 hours

    try:
        os.mkdir('files')
    except OSError:
        pass

    with open(file_name, 'w') as file:
        file.write('[\n')

    with open(credentials_file, 'r') as cred:
        credentials = json.load(cred)
        username = credentials['username']
        password = credentials['password']
        if not username or not password:
            print('Please enter your GitHub credentials in the file credentials.json to start crawling.')
            exit()
        basicAuthCredentials = (username, password)

    t = time.time()
    while repos_crawled < crawl_goal:
        try:
            wait()
            repos = retrieve_repo(start_with + repos_crawled)
            for name in list(map(lambda repo: repo['full_name'], repos)):
                print(f'Retrieving repo {name} ...')
                repos_crawled += 1

                wait()
                langs = retrieve_languages(name)

                wait()
                commits = retrieve_commits(name)

                repo_dict = {'repository': name,
                             'languages': langs,
                             'commits': commits}
                with open(file_name, 'a+', encoding='utf8') as file:
                    if repos_crawled > 1:
                        file.write(',\n')
                    file.write(json.dumps(repo_dict, ensure_ascii=False))
            time.sleep(wait)
        except CrawlerException as e:
            repos_crawled += 1
            print(e)


def main():
    atexit.register(close_file)
    crawl_repos()


if __name__ == "__main__":
    main()
