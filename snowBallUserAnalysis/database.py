#!/usr/bin/env python
import pymongo
import datetime
from pymongo import MongoClient

class Database:
    def __init__(self):
        try:
            client = MongoClient('127.0.0.1', 27017)
            print "Connected successfully!!!"
        except pymongo.errors.ConnectionFailure, e:
           print "Could not connect to MongoDB: %s" % e
        self.db = client['xq']
        self.data = self.db['unit']

        self.extract_db = client['extract']
        self.extract_users = self.extract_db['users']
        self.user_timeline = self.extract_db['user_timeline']

    def insertAUserChange(self, userid, data):
        userid = str(int(userid))
        userInfo = self.user_timeline.find_one({"_id": userid})
        if userInfo == None:
            self.user_timeline.insert_one({"_id": userid})
            userInfo = {"_id": str(int(userid)), "timeline":{}}
        record = {}
        for entry in data["list"]:
            stockID = entry.keys()[0]
            record[stockID] = {}
            record[stockID]["current_price"] = entry[stockID]["current_price"]
            if entry[stockID]["prev_price"] == None:
                record[stockID]["isbuy"] = True
                record[stockID]["amount"] = entry[stockID]["to_value"]
            else:
                if entry[stockID]["to_value"] - entry[stockID]["from_value"] > 0:
                    record[stockID]["isbuy"] = True
                    record[stockID]["amount"] = entry[stockID]["to_value"] - entry[stockID]["from_value"]
                else:
                    record[stockID]["isbuy"] = False
                    record[stockID]["amount"] = entry[stockID]["from_value"] - entry[stockID]["to_value"]
                    record[stockID]["prev_price"] = entry[stockID]["current_price"]
        userInfo["timeline"][str(int(data["time"]))] = record
        self.user_timeline.update({'_id': userid}, userInfo)

    def insertAUnit(self, userid, id, slope, covariance, valid):
        userInfo = self.extract_users.find_one({"_id": userid})
        if userInfo == None:
            self.extract_users.insert_one({"_id": userid})
            userInfo = {"_id": userid, "units": {}}

        if valid:
            userInfo["units"]["id"] = {"revenue_slope" : slope, "revenue_covariance": covariance, "valid": True}
            print "insert"
        else:
            userInfo["units"]["id"] = {"valid": False}
        self.extract_users.update({'_id': userid}, userInfo)


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

# print db
# collection = db.my_collection
# doc = {"name":"Alberto","surname":"Negron","twitter":"@Altons"}
# print collection
# collection.insert(doc)
# print 'done'
# print post_id
