#!/usr/bin/env python
import time
import database
import crawler
from multiprocessing import Process

database = database.Database()

pinID = database.getAnEmptyPin()
userID = database.getAnEmptyUser()

if pinID == None:
    pinID = '121949102380799662'
    database.addPinID(pinID)
if userID == None:
    userID = 'danigriffithsm'
    database.addUserID(userID)

def minePin(id, database):
    my_crawler = crawler.Crawler()
    pinID = id
    print pinID
    while True:
        last_time = time.time()
        info = my_crawler.populatePinInfo(pinID)
        logText = "populate Pin: " + pinID + " got " + str(len(info["pinedUser"])) + " pinedUser and " + str(len(info["likedUser"])) + " likedUser in " + str(time.time() - last_time) + " second\n"
        text_file = open("pin_log.txt", "a")
        text_file.write(logText)
        text_file.close()
        database.addPinInfo(pinID, info)
        pinID = database.getAnEmptyPin()
        while pinID == None:
            print "waiting"
            time.sleep(50)
            pinID = database.getAnEmptyPin()
        pinID = pinID["_id"]

def mineUser(id, database):
    my_crawler = crawler.Crawler()
    userID = id
    print userID
    while True:
        last_time = time.time()
        info = my_crawler.populateUserInfo(userID)
        logText = "populate User: " + userID + " got " + str(len(info["pinDict"])) + " Pins and " + str(len(info["likeDict"])) + " likedPin in " + str(time.time() - last_time) + " second\n"
        text_file = open("user_log.txt", "a")
        text_file.write(logText)
        text_file.close()
        database.addUserInfo(userID, info)
        userID = database.getAnEmptyUser()
        while userID == None:
            print "waiting"
            time.sleep(10)
            userID = database.getAnEmptyUser()
        userID = userID["_id"]

p = Process(target=mineUser, args=(userID, database))
p.start()

p1 = Process(target=minePin, args=(pinID, database))
p1.start()
