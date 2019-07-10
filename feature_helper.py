import unicodedata
import json


def process_commits(commits):
    good_commits = []
    for commit in commits:
        commit = commit.strip()  # remove trailing spaces
        commit = "".join(ch for ch in commit if unicodedata.category(ch)[0] != "C")  # remove control characters
        good_commits.append(commit)
    return good_commits


def get_relevant_langs(languages):
    relevant_languages = []
    total = 0.0
    num_languages = len(languages.keys())
    for lang in languages.keys():
        total += languages[lang]
    print(total, num_languages)
    for lang in languages.keys():
        if languages[lang] >= total / num_languages:
            relevant_languages.append(lang)
    return relevant_languages


def main():
    features = []
    labels = []
    with open('files/repos') as file:
        repos = json.load(file)
        for repo in repos:
            name = repo["repository"]
            languages = get_relevant_langs(repo["languages"])
            commits = process_commits(repo["commits"])

            print(f'Name: {name}')
            print(f'Languages: {languages}')
            print(f'Commits: {commits}')
            print()

            for commit in commits:
                features.append(commit)
                labels.append(languages)

    if len(features) != len(labels):
        print('Unequal amount of features and labels. Something went horribly wrong')

    print(f'{len(features)} feature extracted: {features}')
    print(f'{len(labels)} feature extracted: {labels}')

    with open('files/features', 'w') as file:
        file.write(json.dumps(features))

    with open('files/labels', 'w') as file:
        file.write(json.dumps(labels))


if __name__ == "__main__":
    main()
