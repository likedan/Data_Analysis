import sys
sys.path.append('chinese_stock_api')
from cstock.request import Requester
from cstock.yahoo_engine import YahooEngine
import database
import time

engine = YahooEngine()
requester = Requester(engine)
stock_obj = requester.request('000626',("2014-03-04","2014-03-06"))
print stock_obj[0].as_dict()

def calculateMaxGain(data):
    print "data  "


db = database.Database()
for entry in db.data.find():
    if "trade_timetable" in entry:
	print(entry["id"])
        trade_timetable = entry["trade_timetable"]
        for trade in trade_timetable:
            t = time.strftime("%Y-%m-%d", time.localtime(trade["time"]/1000 + 13*60*60))
            print(t)
	print("---------")
