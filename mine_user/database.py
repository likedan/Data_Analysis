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
        self.db = client['extract']
        self.data = self.db['units']

# add a pin without detail info
    def add_unit_info(self, info):
        if self.data.find_one({"_id": info["symbol"]}) == None:
            self.data.update({"_id": info["symbol"]}, info, upsert=True)
            print "add" + info["symbol"]
