from Crawler import Crawler
from DefaultVariables import *

c = Crawler()
c.get_stock_list_with_url(STOCK_MARKET_URLS["NASDAQ"])