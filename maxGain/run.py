
import database
import time
import engine

eng = engine.Engine()

def calculateMaxGain(data, engine):
    for stock in data["list"]:
        stockName = stock.keys()[0][2:]
        amount = 0
        if stock[stockName]["from_value"] == None:
            amount = stock[stockName]["to_value"]
        elif stock[stockName]["to_value"] - stock[stockName]["from_value"] > 0:
            amount = stock[stockName]["to_value"] - stock[stockName]["from_value"]
        price = stock[stockName]["current_price"]
        highest = eng.getNextThreeDaysHighest(float(data["time"])/1000.0 + 13*60*60, stockName)
        print price
        print highest


db = database.Database()
for entry in db.data.find():
    if "trade_timetable" in entry:
	print(entry["id"])
        trade_timetable = entry["trade_timetable"]
        for trade in trade_timetable:
            calculateMaxGain(trade, eng)

	print("---------")
