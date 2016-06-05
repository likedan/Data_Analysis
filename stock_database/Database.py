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
        self.full_symbols_list = self.db['full_symbol_list']
        self.alphabet_symbols_list = self.db['alphabet_symbol_list']
