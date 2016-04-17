import json
import os
import pandas as pd
import numpy as np
from sklearn import cross_validation
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

##sentiment
#has price
#has time
#has link
#is a reply
#time posting

filenames = ['dgaz','dust','dwti','jdst','jnug','nugt','ugaz','uso','uwti']
filenames = ['jdst']

time = ["previous", "year", "years", "overview", "month", "months", "latest", "following", "during",
        "daily", "recent", "recently", "present", "next", "since", "last", "days", "day", "coming", "soon", "today"]
operations = ["buy", "bought", "buying", "buys", "sell", "sold", "sells", "selling", "long", "short", "entry", "point",
             "hold", "holding", "holds", "held", "trade", "trading", "traded", "enter", "entered", "share", "sharing",
             "shared", "low", "high", "lower", "higher", "lowest", "highest", "drop", "dropped"]

time = set(time)
operations = set(operations)

os.chdir(os.getcwd() + '\data')
data = []
for filename in filenames:
    posts = []
    with open('cleanMessages_' + filename + '.json', encoding="utf8") as f:
        for line in f:
            posts.append(json.loads(line))
    
    for post in posts[0]:
        features = dict()
        features['length'] = post['length']
        features['hasPrice'] = post['hasPrice']
        features['hasLink'] = post['hasLink']
        features['isReply'] = 0
        features['hasTime'] = 0
        features['hasOperation'] = 0
    
        for word in post['body'].split():
            if(features['hasTime'] != 1 and word in time):
                features['hasTime'] = 1
                
            if(features['hasOperation'] != 1 and word in operations):
                features['hasOperation'] = 1
        
        if(post['in_reply_to_message_id'] != None):
            features['isReply'] = 1
        
        features['isReply'] = 0
        try:
            features['label'] = (post['total_likes'] > 4 or post['conversation']['replies']> 10)
        except:
            features['label'] = 0
        data.append(features)

#data = np.random.choice(data, replace = False, size = int(len(data)*.3))
df = pd.DataFrame(data, dtype = np.int32)

labels = df['label']
df.drop('label', axis=1, inplace=True)
clf = RandomForestClassifier(n_estimators = 200)

#X_train, X_test, y_train, y_test = cross_validation.train_test_split(df, labels, test_size=0.3, random_state=0)
#predicted = clf.fit(X_train, y_train).predict(X_test)
#print(metrics.accuracy_score(y_test, predicted))

scores = cross_validation.cross_val_score(clf, df, labels, cv=10)
print(scores)