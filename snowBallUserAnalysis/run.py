
import database
import time
import engine
from scipy import stats
import numpy as np

# eng = engine.Engine()
# eng.getNextThreeDaysHighest(float(1447375729136)/1000.0, "601216")

# def calculateMaxGain(data, engine):
#     for stock in data["list"]:
#         stockName = stock.keys()[0]
#         stockNum = stockName[2:]
#         amount = 0
#         # highest = eng.getNextThreeDaysHighest(float(data["time"])/1000.0, stockNum)
#
#         if stock[stockName]["from_value"] == None:
#             amount = stock[stockName]["to_value"]
#         elif stock[stockName]["to_value"] - stock[stockName]["from_value"] > 0:
#             amount = stock[stockName]["to_value"] - stock[stockName]["from_value"]
#         price = stock[stockName]["current_price"]
#         print price
#         print highest


db = database.Database()
for entry in db.data.find():
    if "revenue_trend" in entry:
        revenue_trend = entry["revenue_trend"]
        netValue = []
        for point in revenue_trend:
            netValue.append(point["value"])
        X = np.arange(len(netValue))

        slope, intercept, r_value, p_value, std_err = stats.linregress(X, np.array(netValue))

        print slope
        print intercept
        print r_value
        print p_value

#     if "trade_timetable" in entry:
# 	print(entry["id"])
#         trade_timetable = entry["trade_timetable"]
#         for trade in trade_timetable:
#             calculateMaxGain(trade, eng)
#
# 	print("---------")
