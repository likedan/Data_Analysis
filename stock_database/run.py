from Crawler import Crawler
from DefaultVariables import *
from Database import Database
import threading
import time

db = Database()
symbol_file_name = "symbols.txt"

symbol_list = []

with open(symbol_file_name, 'rb') as symbolFile:
    for row in symbolFile:
        symbol = row.split("\t")[0]
        symbol_list.append(symbol)

symbol_set = set(symbol_list)

five_letter_stock = []

db_symbol_list = []
for x in db.raw_data.find().distinct("symbol"):
    if len(x) > 4:
        five_letter_stock.append(x)
    db_symbol_list.append(x)
db_symbol_set = set(db_symbol_list)

print symbol_set - db_symbol_set
print len(symbol_set - db_symbol_set)

print five_letter_stock
# for info in db.raw_data.find():
#     info["raw_data"][""]