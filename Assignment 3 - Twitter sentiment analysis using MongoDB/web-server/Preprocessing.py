
# coding: utf-8



import json
import re
import nltk
import numpy as np
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer


with open('tagged_data.json', 'r') as f:
    read_data = f.read()
f.closed


#Reading the annotated tweets from file downloaded from Mongo
data  = json.loads(read_data)
#Splitting dataset in training (80) and test(20) set
test = []
for item in data:
    i = np.random.randint(0,101)
    if i < 20:
        test.append(item)
        data.remove(item)
len(test), len(data)


#spanish stopwords
spanish_stopwords = set(stopwords.words('spanish'))
spanish_stopwords.add('q')
spanish_stopwords.add('dice')
spanish_stopwords.add('lleva')
def get_sentiments(tweets):
    sentiments = []
    for tweet in tweets:
        sentiments.append(int(tweet['sentiment']))
    return sentiments
def tweet_to_words(tweet):
    # Preprocessing step 1: Removing all links
    result = re.sub(r"http\S+", "", tweet['text'])
    tweet['text'] = result
    # Preprocessing step 2: Removing all mentions, non-letters, and converting all strings to lower case
    result = re.sub(r"@\S+", "", tweet['text'])
    result = re.sub(r"[^A-Za-záéíóúÁÉÍÓÚñ]", " ", result)
    tweet['text'] = result.lower()
    # Preprocessing step 3: Removing all spanish stopwords, tokenizing
    words = tweet['text'].split()
    result = [w for w in words if not w in spanish_stopwords]
    result = " ".join(result)
    tweet['text'] = result
    return tweet

sentiments = get_sentiments(data)
for item in data:
    item = tweet_to_words(item)

#Initialize Count Vectorizer
vectorizer = CountVectorizer(analyzer = "word",                                tokenizer = None,                                 preprocessor = None,                              stop_words = None,                                max_features = 2000) 
tweet_vocabulary = []
for tweet in data:
    tweet_vocabulary.append(tweet['text'])

train_data_features = vectorizer.fit_transform(tweet_vocabulary)
train_data_features = train_data_features.toarray()
import numpy as np 
vocab = vectorizer.get_feature_names()
dist = np.sum(train_data_features, axis=0)
res = []
for tag, count in zip(vocab, dist):
    res.append({"count": count, "tag" : tag})
    #print(tag, count)
#sorted(res, key=itemgetter('count'), reverse=True) 


from sklearn.ensemble import RandomForestClassifier
from sklearn.naive_bayes import MultinomialNB
bayes = MultinomialNB()
bayes = bayes.fit(train_data_features, sentiments)
forest = RandomForestClassifier(n_estimators = 100) 
forest = forest.fit(train_data_features, sentiments)


len(test)

# Cleaning test data
clean_test_reviews = [] 
for item in test:
    clean_review = tweet_to_words(item)
    clean_test_reviews.append(clean_review['text'])

test_data_features = vectorizer.transform(clean_test_reviews)
test_data_features = test_data_features.toarray()
result = forest.predict(test_data_features)
result_bayes = bayes.predict(test_data_features)


from sklearn.metrics import precision_recall_fscore_support as score
from sklearn.metrics import confusion_matrix

y_test = get_sentiments(test)
# Calculate performance metrics for Tree classifier
precision, recall, fscore, support = score(y_test, result, labels=[-1, 0 ,1])

print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))


precision, recall, fscore, support = score(y_test, result_bayes, labels=[-1, 0 ,1])
# Calculate performance metrics for Naive Bayes classifier
print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))

# Calculate confusion matrix for Tree classifier
print(confusion_matrix(y_test, result, labels=[-1, 0, 1]))

# Calculate confusion matrix for Naive Bayes classifier
print(confusion_matrix(y_test, result_bayes, labels=[-1, 0, 1]))

##Repeating above steps for polarity 

def get_polarity(tweets):
    polarity = []
    for tweet in tweets:
        polarity.append(int(tweet['polarity']))
    return polarity
polarity = get_polarity(data)

forest_polarity = RandomForestClassifier(n_estimators = 100) 
forest_polarity = forest_polarity.fit(train_data_features, polarity)
result_polarity = forest_polarity.predict(test_data_features)
y_test_polarity = get_polarity(test)

precision, recall, fscore, support = score(y_test_polarity, result_polarity, labels=[-2, -1, 0 ,1, 2])

print('precision: {}'.format(precision))
print('recall: {}'.format(recall))
print('fscore: {}'.format(fscore))
print('support: {}'.format(support))

print(confusion_matrix(y_test_polarity, result_polarity, labels=[-2, -1, 0, 1, 2]))

clean = []
clean.append(tweet_to_words(data[200])['text'])
test_data_features = vectorizer.transform(tweet_to_words(data[200])['text'])

print(test_data_features)




forest_polarity.predict(test_data_features)




count_sent1 = 0
count_sent0 = 0
count_sent_1 = 0
count_pol1 = 0
count_pol2 = 0
count_pol0 = 0
count_pol_1 = 0
count_pol_2 = 0
for tweet in test:
    if tweet['sentiment'] == -1:
        count_sent_1 += 1
    elif tweet['sentiment'] == 0:
        count_sent0 += 1
    elif tweet['sentiment'] == 1:
        count_sent1 += 1
    if tweet['polarity'] == -2:
        count_pol_2 += 1
    elif tweet['polarity'] == -1:
        count_pol_1 += 1
    elif tweet['polarity'] == 0:
        count_pol0 += 1
    elif tweet['polarity'] == 1:
        count_pol1 += 1
    elif tweet['polarity'] == 2:
        count_pol2 += 1
        
print("[" + str(count_sent_1) + ", " + str(count_sent0) + ", "+ str(count_sent1) + "]")
print("[" + str(count_pol_2) + ", " + str(count_pol_1) + ", " + str(count_pol0) + ", "+ str(count_pol1)
      + ", " + str(count_pol2) + "]")


# In[ ]:



