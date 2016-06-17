#!/usr/bin/env python
from DefaultVariables import *
import pymongo
from pymongo import *
from bson.objectid import ObjectId
import datetime


class Database:
    def __init__(self):
        try:
            self.client = MongoClient('127.0.0.1', 27017)
            print "create db instance"
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
        self.db = self.client[DATABASE_NAME]
        self.currency_list = self.db['currency_list']

    def get_currency_list(self):
        c_list = [currency for currency in self.currency_list.find()]
        return c_list

    def get_available_currency_list(self):
        collections = [collection for collection in self.db.collection_names() if self.currency_list.find({"symbol": collection}).count() == 1]
        return collections

    def close(self):
        self.client.close()