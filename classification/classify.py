import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

with open('../files/features.json', encoding='utf8') as file:
    features = json.load(file)

with open('../files/labels.json', encoding='utf8') as file:
    labels = json.load(file)

# transform labels into numerical categories (e.g. Java => 1, Python => 2)
labels_numerical = []
categories = {}
for i, lab in enumerate(labels):
    lab = lab[0]
    if lab not in categories:
        categories[lab] = i
    labels_numerical.append(categories[lab])

# Build and fit the tfidf transformation
tfidf = TfidfVectorizer(min_df=1, smooth_idf=True, stop_words=None)
X = tfidf.fit_transform(features).toarray()

# Split the data into training and test set
n = 2000
X_train, X_test, Y_train, Y_test = train_test_split(X[:n], labels_numerical[:n], test_size=0.2, random_state=0)

print('Fitting classifier')
classifier = RandomForestClassifier(n_estimators=200, random_state=0, min_samples_leaf=1)
classifier.fit(X_train, Y_train)

# Print out the predicted vs actual values
y_pred = classifier.predict(X_test)
corr = 0
wrong = 0
for i in range(0, len(y_pred)):
    for k in categories.keys():
        if categories[k] == y_pred[i]:
            if y_pred[i] == Y_test[i]:
                corr += 1
                print('✓', end=' ')
            else:
                wrong += 1
                print('X', end=' ')
            print(k, end=', ')  # predicted value

    for k in categories.keys():
        if categories[k] == Y_test[i]:
            print(k)  # actual value

# Print out results
print('\nCorrect:', corr)
print('Wrong:', wrong)
print('Languages considered:', len(categories.keys()))
print('\nClassifier Score:', classifier.score(X_test, Y_test) * 100, '%')
