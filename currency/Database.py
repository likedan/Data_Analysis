#!/usr/bin/env python
from DefaultVariables import *
import pymongo
from pymongo import *
from bson.objectid import ObjectId
import datetime, time
import Helper

class Database:
    def __init__(self):
        try:
            self.client = MongoClient('127.0.0.1', 27017)
            print "create db instance"
        except pymongo.errors.ConnectionFailure, e:
            print "Could not connect to MongoDB: %s" % e
        self.db = self.client[DATABASE_NAME]
        self.currency_list = self.db['currency_list']
        self.realtime_data = self.db["realtime_data"]

    def get_currency_list(self):
        c_list = [currency for currency in self.currency_list.find()]
        return c_list

    def get_available_currency_list(self):
        collections = [collection for collection in self.db.collection_names() if self.currency_list.find({"symbol": collection}).count() == 1]
        return collections

    def get_one_day_currency_data(self, symbol, date):

        date = int(date)
        Helper.is_valid_symbol(symbol)
        Helper.is_valid_date(date)

        return self.db[symbol].find_one({"date": date})

    def get_range_currency_date(self, symbol, start, end):

        start = int(start)
        end = int(end)
        Helper.is_valid_symbol(symbol)
        Helper.is_valid_date(start)
        Helper.is_valid_date(end)
        start_time = int(time.mktime(datetime.datetime.strptime(str(start), "%Y%m%d").timetuple()))
        end_time = int(time.mktime(datetime.datetime.strptime(str(end), "%Y%m%d").timetuple()))
        results = []
        for day_date in self.db[symbol].find({'unix_time': {'$gte': start_time, '$lte': end_time}}):
            results.append(day_date)
        results = sorted(results, key=lambda k: k['unix_time'])
        return results

    def close(self):
        self.client.close()