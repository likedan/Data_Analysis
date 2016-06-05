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
        self.db = client['Stock_Database']
        self.symbol_list = self.db['symbol_list']

    def get_full_stock_dict(self):
        result_dict = {}
        for item in self.symbol_list.find():
            result_dict[item["symbol"]] = item["url"]
        return result_dict

    def get_alpha_stock_dict(self):
        result_dict = {}
        for item in self.symbol_list.find({"isalpha": True}):
            result_dict[item["symbol"]] = item["url"]
        return result_dict