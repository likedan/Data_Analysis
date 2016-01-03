import sys
sys.path.append('strategies')
import macd
from datetime import date, timedelta

stock_list = []
with open('downloadData/stockList') as f:
    lines = f.readlines()
    for line in lines:
        stock = line
        if line[-1] == "\n":
            stock = line[:(len(line)-1)]
        stock_list.append(stock)

# print stock_list
macddd = macd.MACD("CMG")
macddd.generate_features(1)
print "done"
# macddd.generate_features(2)
# print "done"
# macddd.generate_features(3)
# print "done"
# macddd.generate_features(4)
# print "done"
# macddd.generate_features(5)
# print "done"

macddd.train(150)
macddd.predict(150)
# macddd.plot()
