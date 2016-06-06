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

for key in alpha_stock_dict.keys()[0:2]:
    crawler.download_historical_data(alpha_stock_dict[key])


# delisted_stocks = ["AYE","COMS","SE","ADCT","ACS","ACV","ABS","AL","ANG","AW","AH","AT","ANR","AZA","AGC","AM","APCC","ASO","ANDW","BUD","ABI","ACK"]

# for s in delisted_stocks:
#     if not (s in full_stock_dict):
#         print s