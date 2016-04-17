#@author: Ziyan Liu

import json
import string
import re
import os
import numpy as np

stop_word = set()
big_dictionary = {}
numLikes = []
numReplies = []
numReShares = []
filenames = ['dgaz','dust','dwti','jdst','jnug','nugt','ugaz','uso','uwti']

message_types = set()
sentimentsClass = set()
sentimentsName = set()
with open('stopWords.txt') as word:
    for line in word:
        stop_word.add(line.replace('\n', ''))
        
os.chdir(os.getcwd() + '\data')

translator = str.maketrans({key: None for key in string.punctuation})
for filename in filenames:
    word_dictionary = {}
    posts = []
    with open(filename + '.json', encoding="utf8") as f:
        for line in f:
            posts.append(json.loads(line))
    
    for post in posts:
        numLikes.append(post['total_likes'])
        numReShares.append(post['total_reshares'])
        try:
            numReplies.append(post['conversation']['replies'])
        except KeyError:
            numReplies.append(0)
        
        msg = post['body']
        key = post['id']
        post['hasPrice'] = 0
        post['hasLink'] = 0
        try:
            sentimentsClass.add(post['sentiment']['class'])
            sentimentsName.add(post['sentiment']['name'])
        except:
            sentimentsName.add('None')
            sentimentsClass.add('None')
            
        message_types.add(post['message_type'])
        msgBody = []
        post['length'] = len(msg.split(" "))
        for word in msg.split(" "):
            if (len(word) > 0):
                if (word[0] != '$'):
                    price = re.search('\$*([0-9]+)\.([0-9][0-9])', word)
                    if(price):
                        post['hasPrice'] = 1
                    
                    price = re.search('www\..+|http.+', word)
                    if(price):
                        post['hasLink'] = 1
                    
                    word = re.sub('www\..+|http.+', '', word)
                    word = word.translate(translator).lower()
                    word = re.sub(r'\n|\r|\t|[^\x00-\x7F]+|[0-9]+','',word)
                    if (len(word) > 0):
                        if(word not in word_dictionary.keys()):
                            word_dictionary[word] = 0
                        word_dictionary[word] = word_dictionary[word]+1
                    
                        if(word not in big_dictionary.keys()):
                            big_dictionary[word] = 0
                        big_dictionary[word] = big_dictionary[word]+1
                        
                        if(word not in filenames):
                            msgBody.append(word)
            
        post['body'] = " ".join(msgBody)
                        
    outDict = {k:v for k, v in word_dictionary.items() if v >= 500 and not (k in stop_word or k in filenames)}

    sortedKey = sorted(outDict.items(), key = lambda x : outDict[x[0]], reverse =True)
    with open('output_' + filename + '.txt', 'w') as fp:
        for pair in sortedKey:
            fp.write(pair[0] + ":" + str(pair[1]) + "\n")
            
    with open('cleanMessages_' + filename + '.json', 'w') as fp:
        json.dump(posts, fp)

numLikes = np.array(numLikes)
numReplies = np.array(numReplies)
numReShares = np.array(numReShares)

meanLikes = np.mean(numLikes)
stdLikes = np.std(numLikes)
meanReplies = np.mean(numReplies)
stdReplies = np.std(numReplies)
meanReShares = np.mean(numReShares)
stdReShares = np.std(numReShares)

print(str(meanLikes) + ',' +  str(stdLikes))
print(str(meanReplies) + ',' +  str(stdReplies))
print(str(meanReShares) + ',' +  str(stdReShares))

#0.901142723514, 1.7616721766
#1.67298477493, 5.65112301965

#with open('bigoutput.json', 'w') as fp:
#    json.dump(big_dictionary, fp)
