
import database
import time
import engine
from scipy import stats
import numpy as np



# def calculateMaxGain(datanext, data, engine, trend):
#
#     for entry in trend:
#         if
#
#     for stock in data["list"]:
#         stockName = stock.keys()[0]
#         stockNum = stockName[2:]
#
#         if datanext["time"]
#         for s in datanext["list"]:
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



def calculateEntireLinearRegression():
    db = database.Database()
    for entry in db.data.find():
        if "revenue_trend" in entry:
            if len(entry["trade_timetable"]) >= 5:
                revenue_trend = entry["revenue_trend"]
                netValue = []
                for point in revenue_trend:
                    netValue.append(point["value"])
                X = np.arange(len(netValue))

                slope, intercept, r_value, p_value, std_err = stats.linregress(X, np.array(netValue))

                db.insertAUnit(entry["owner"], entry["id"], slope, r_value, True)
                print slope
                print intercept
                print r_value
                print "~~~~~~"
            else:
                db.insertAUnit(entry["owner"], entry["id"], 0, 0, False)

def buildUserOrientedDatabase():
    db = database.Database()
    count = 0
    for entry in db.data.find():
        if "trade_timetable" in entry:
            for diction in entry["trade_timetable"]:
                db.insertAUserChange(entry["owner"], diction)

def calculateThreeDaysGain():
    eng = engine.Engine()
    eng.getNextThreeDaysHighest(float(1447375729136)/1000.0, "601216")

    db = database.Database()
    for entry in db.data.find():
        if "trade_timetable" in entry:
            if len(entry["trade_timetable"]) >= 5:
                trade_timetable = entry["trade_timetable"]
                revenue_trend = entry["revenue_trend"]
                for index in xrange(4):
                    calculateMaxGain(trade_timetable[index], trade_timetable[index + 1], eng, revenue_trend)

def countTimeline():
    db = database.Database()
    count = 0
    total = 0
    # for entry in db.data.find():
    #     if "trade_timetable" in entry:
    #         if len(entry["trade_timetable"]) > 5:
    #             count = count + 1
    #             total = total + len(entry["trade_timetable"])
    #             print total
    # print count
    # count = 0
    # total = 0
    for entry in db.user_timeline.find():
        if len(entry["timeline"]) > 5:
            total = total + len(entry["timeline"])
            count = count + 1
    print count
    print total


# data1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(1447257600))
# print data1
#
# for index in xrange(4):
#     print index
buildUserOrientedDatabase()
countTimeline()

#
# 	print("---------")
