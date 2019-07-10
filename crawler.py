import urllib.request
import urllib.error
import json
import time

rps = 0.71  # max possible requests per second (rps) allowed by public API
file_name = 'files/repos'

def retrieve_repo(since):
    time.sleep(rps)
    with urllib.request.urlopen(f'https://api.github.com/repositories?since={since}') as f:
        content = f.read().decode('utf-8')
        repo_list = json.loads(content)
        return repo_list


def retrieve_languages(name):
    time.sleep(rps)
    with urllib.request.urlopen(f'https://api.github.com/repos/{name}/languages') as f:
        content = f.read().decode('utf-8')
        language_list = json.loads(content)
        return language_list


def retrieve_commits(name):
    time.sleep(rps)
    with urllib.request.urlopen(f'https://api.github.com/repos/{name}/commits') as f:
        content = f.read().decode('utf-8')
        commits_list = json.loads(content)
        return list(map(lambda commit: commit['commit']['message'], commits_list))


def crawl_repos():
    repos_crawled = 0
    crawl_goal = 5000  # max possible in one hour

    with open(file_name, 'w') as file:
        file.write('[\n')

    while repos_crawled < crawl_goal:
        try:
            repos = retrieve_repo(repos_crawled)
            for name in list(map(lambda repo: repo['full_name'], repos)):
                print(f'Retrieving repo {name} ...')
                langs = retrieve_languages(name)
                commits = retrieve_commits(name)
                repo_dict = {'repository': name,
                             'languages': langs,
                             'commits': commits}
                repos_crawled += 1
                with open(file_name, 'a+') as file:
                    if repos_crawled > 1:
                        file.write(',\n')
                    file.write(json.dumps(repo_dict))
        except urllib.error.HTTPError:
            print('Public API limits exhausted')
            break

    with open(file_name, 'a+') as file:
        file.write('\n]')


def main():
    crawl_repos()


if __name__ == "__main__":
    main()
