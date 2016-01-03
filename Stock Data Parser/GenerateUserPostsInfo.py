# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 21:08:04 2016

@author: Kangyan Zhou
"""

import json

class User:
    def __init__(self, _id):
        self.id = _id
        self.numOfLikes = 0
        self.numOfPosts = 0
        self.numOfReplies = 0
        self.originPostID = []
        self.highestLikes = 0
        self.highestReplies = 0
        self.avgLikes = 0
        self.avgReplies = 0
        
    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            indent=4)

posts = []
with open('dgaz.json', encoding="utf8") as f:
    for line in f:
        posts.append(json.loads(line))

users = {}
value = {}
for post in posts:
    userid = post['user']['id']
    if(userid not in users.keys()):
        users[userid] = User(_id = userid)
    
    user = users[userid]
    user.numOfLikes = user.numOfLikes + post['total_likes']
    user.numOfPosts = user.numOfPosts + 1
    try:
        user.numOfReplies = user.numOfReplies + post['conversation']['replies']
    except KeyError:
        continue
    
    if(post['conversation']['replies'] > users[userid].highestReplies):
        users[userid].highestReplies = post['conversation']['replies']

    if(post['total_likes'] > users[userid].highestLikes):
        users[userid].highestLikes = post['total_likes'] 
    
    user.originPostID.append(post['id'])
    users[userid] = user
    if(post['conversation']['replies'] > 30 or post['total_likes'] > 15):
        value[post['id']] = post['body']

for _id, user in users.items():
    try:
        user.avgLikes = (user.numOfLikes - user.highestLikes)/(user.numOfPosts - 1)
        user.avgReplies = (user.numOfReplies - user.highestReplies)/(user.numOfPosts - 1)
    except ZeroDivisionError:
        user.avgLikes = 0
        user.avgReplies = 0

with open('output_dgaz.json', 'w') as out:
    for user in users.values():
        if(user.avgReplies > 5 and user.numOfPosts >= 5 and user.avgLikes > 3):
            out.write(user.to_JSON())
            out.write('\n')

with open('valuable_post_dgaz.json', 'w') as out:
    json.dump(value, out, separators=('\n', ':'))