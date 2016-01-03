
import database
import time
import engine

db = database.Database()
# eng = engine.Engine()
# eng.getNextThreeDaysHighest("300339","300339")
#
# def calculateMaxGain(data):
#     t = time.strftime("%Y-%m-%d", time.localtime(data["time"]/1000 + 13*60*60))
#     for stock in data["list"]:
#         stockName = stock.keys()[0]
#         amount = 0
#         if stock[stockName]["from_value"] == None:
#             amount = stock[stockName]["to_value"]
#         elif stock[stockName]["to_value"] - stock[stockName]["from_value"] > 0:
#             amount = stock[stockName]["to_value"] - stock[stockName]["from_value"]
#         price = stock[stockName]["current_price"]
#         print amount
#         print price



# db = database.Database()
# for entry in db.data.find():
#     if "trade_timetable" in entry:
# 	print(entry["id"])
#         trade_timetable = entry["trade_timetable"]
#         for trade in trade_timetable:
#             calculateMaxGain(trade)
#
# 	print("---------")
