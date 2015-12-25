#!/usr/bin/env python
import pymongo
import datetime
from pymongo import MongoClient
from yahoo_finance import Share
from datetime import date, timedelta

client = MongoClient('127.0.0.1', 27017)
db = client['stock_historical_data']

stock_list = []
with open('stockList') as f:
    lines = f.readlines()
    for line in lines:
        stock = line
        if line[-1] == "\n":
            stock = line[:(len(line)-1)]
        stock_list.append(stock)

for stock_name in stock_list:
    stock = db[stock_name]
    last_updated_time = stock.find_one({"_id": "last_updated_time"})
    if last_updated_time == None:
        last_updated_time = "1995-11-27"
        stock.insert_one({"_id": "last_updated_time", "date": "1995-11-27"})
    else:
        last_updated_time = last_updated_time["date"]

    yahoo = Share(stock_name)
    data = yahoo.get_historical(last_updated_time, date.today().strftime('%Y-%m-%d'))
    for entry in data:
        entry["_id"] = entry["Date"]
        stock.update({"_id": entry["_id"]}, entry ,upsert=True)
    stock.update({"_id": "last_updated_time"}, {"date": (date.today() - timedelta(days = 1)).strftime('%Y-%m-%d')} ,upsert=True)
    print stock_name
    print len(data)
# # add a pin without detail info
#     def addPinID(self, id):
#         if self.pins.find_one({"_id": id}) == None:
#             info = {"_id": id, "isPopulated" : False}
#             self.pins.insert_one(info)
#             print "inserted"
#
# # add a user without detail info
#     def addUserID(self, id):
#         if self.users.find_one({"_id": id}) == None:
#             info = {"_id": id, "isPopulated" : False}
#             self.users.insert_one(info)
#             print "inserted"
#
# # get random user that haven't been populated
#     def getAnEmptyUser(self):
#         try:
#             return self.users.find_one({"isPopulated" : False})
#         except Exception as e:
#             print "no pin"
#             return None
#
# # get random pin that haven't been populated
#     def getAnEmptyPin(self):
#         try:
#             return self.pins.find_one({"isPopulated" : False})
#         except Exception as e:
#             print "no user"
#             return None
#
# # add the information on a Pin and add the userIDs
#     def addPinInfo(self, id, info):
#         information = self.pins.find_one({"_id": id})
#         if information != None and information["isPopulated"] == False:
#             information["isPopulated"] = True
#             if len(info["likedUser"]) > 0:
#                 information["likedUser"] = info["likedUser"]
#                 userList = []
#                 for user in information["likedUser"]:
#                     if self.users.find_one({"_id": user}) == None:
#                         userList.append({"_id": user, "isPopulated" : False})
#                 if len(userList) > 0 :
#                     print userList
#                     self.users.insert(userList)
#             if len(info["pinedUser"]) > 0:
#                 information["pinedUser"] = info["pinedUser"]
#                 userList = []
#                 for user in information["pinedUser"]:
#                     if self.users.find_one({"_id": user}) == None:
#                         userList.append({"_id": user, "isPopulated" : False})
#                 if len(userList) > 0 :
#                     print userList
#                     self.users.insert(userList)
#             information["imageURL"] = info["imageURL"]
#             self.pins.update({'_id': id}, information)
#
#
#
# # add the information on a User and add the pinIDs
#     def addUserInfo(self, id, info):
#         information = self.users.find_one({"_id": id})
#         print information
#         if information != None and information["isPopulated"] == False:
#             information["isPopulated"] = True
#             information['nickName'] = info['nickName']
#             information["boardCount"] = info["boardCount"]
#             information["pinCount"] = info["pinCount"]
#             information["likeCount"] = info["likeCount"]
#             information["followingCount"] = info["followingCount"]
#             information["followerCount"] = info["followerCount"]
#             if len(info["boardList"]) > 0:
#                 information["boardList"] = info["boardList"]
#             if len(info["likeDict"]) > 0:
#                 information["likeDict"] = info["likeDict"].keys()
#                 pinList = []
#                 for pin in information["likeDict"]:
#                     if self.pins.find_one({"_id": pin}) == None:
#                         pinList.append({"_id": pin, "isPopulated" : False})
#                 if len(pinList) > 0 :
#                     self.pins.insert(pinList)
#                 print pinList
#
#             if len(info["pinDict"]) > 0:
#                 information["pinDict"] = info["pinDict"].keys()
#                 pinList = []
#                 for pin in information["pinDict"] :
#                     if self.pins.find_one({"_id": pin}) == None:
#                         pinList.append({"_id": pin, "isPopulated" : False})
#                 if len(pinList) > 0 :
#                     self.pins.insert(pinList)
#                 print pinList
#
#             self.users.update({'_id': id}, information)
#
# # print db
# # collection = db.my_collection
# # doc = {"name":"Alberto","surname":"Negron","twitter":"@Altons"}
# # print collection
# # collection.insert(doc)
# # print 'done'
# # print post_id
