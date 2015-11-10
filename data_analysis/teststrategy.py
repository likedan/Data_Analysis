import sys
sys.path.append('strategies')
import macd
from datetime import date, timedelta

for day in range(0, 100):
    print day
    macdd = macd.MACD("DGAZ", (date.today() - timedelta(days = day + 200)), (date.today() - timedelta(days = day)))
    macdd.calculate_buying_score()
# macdd.plot()
