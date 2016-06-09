from Crawler import Crawler
from DefaultVariables import *
from Database import Database

crawler = Crawler()

db = Database()
alpha_stock_dict = db.get_alpha_stock_dict()

for key in alpha_stock_dict.keys():

    stock_info = db.symbol_list.find_one({"symbol": key})
    if "isValid" in stock_info:
        print "skip: " + stock_info["symbol"]
    else:
        data = crawler.download_historical_data(key, alpha_stock_dict[key])
        
        if len(data) > 0:
            for entry in data:
                db.upsert_stock_data(key, entry)
            stock_info["isValid"] = True
        else:
            stock_info["isValid"] = False
        db.symbol_list.update({"_id": stock_info["_id"]}, stock_info, True)

# delisted_stocks = ["AYE","COMS","SE","ADCT","ACS","ACV","ABS","AL","ANG","AW","AH","AT","ANR","AZA","AGC","AM","APCC","ASO","ANDW","BUD","ABI","ACK"]

# for s in delisted_stocks:
#     if not (s in full_stock_dict):
#         print s