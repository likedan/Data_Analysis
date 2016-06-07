from Crawler import Crawler
from DefaultVariables import *
from Database import Database

crawler = Crawler()

# for stock_market in STOCK_MARKET_URLS.keys():
#     print stock_market
#     stock_dict = crawler.get_stock_list_with_url(STOCK_MARKET_URLS[stock_market])
#     if len(stock_dict) == 0:
#         raise Exception('No Stock Found!')

#     full_stock_dict.update(stock_dict)

db = Database()
alpha_stock_dict = db.get_alpha_stock_dict()

for key in alpha_stock_dict.keys():

    stock_info = db.symbol_list.find_one({"symbol": key})
    if "isValid" in stock_info:
        print "skip: " + stock_info["symbol"]
    else:
        data = crawler.download_historical_data(alpha_stock_dict[key])
        
        print len(data)
        if len(data) > 0:
            db.db[key].insert_many(data)
            stock_info["isValid"] = True
        else:
            stock_info["isValid"] = False
        db.symbol_list.update({"_id": stock_info["_id"]}, stock_info, True)

# delisted_stocks = ["AYE","COMS","SE","ADCT","ACS","ACV","ABS","AL","ANG","AW","AH","AT","ANR","AZA","AGC","AM","APCC","ASO","ANDW","BUD","ABI","ACK"]

# for s in delisted_stocks:
#     if not (s in full_stock_dict):
#         print s