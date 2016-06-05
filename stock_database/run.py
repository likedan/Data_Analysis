from Crawler import Crawler
from DefaultVariables import *
from Database import Database

crawler = Crawler()

full_stock_dict = {}
for stock_market in STOCK_MARKET_URLS.keys():
    print stock_market
    stock_dict = crawler.get_stock_list_with_url(STOCK_MARKET_URLS[stock_market])
    if len(stock_dict) == 0:
        raise Exception('No Stock Found!')

    full_stock_dict.update(stock_dict)

# database_insert = []
# for key in full_stock_dict.keys():
#     database_insert.append({"symbol":key, "url": full_stock_dict[key]})
# print database_insert
db = Database()
db.symbol_list.insert_many(database_insert)

# stock_only_alphabet = {}

# for key in full_stock_dict.keys():
#     if key.isalpha():
#         stock_only_alphabet[key] = full_stock_dict[key]

# for key in full_stock_dict.keys():
#     print key
#     print crawler.historical_data_exists(full_stock_dict[key])


# delisted_stocks = ["AYE","COMS","SE","ADCT","ACS","ACV","ABS","AL","ANG","AW","AH","AT","ANR","AZA","AGC","AM","APCC","ASO","ANDW","BUD","ABI","ACK"]

# for s in delisted_stocks:
#     if not (s in full_stock_dict):
#         print s