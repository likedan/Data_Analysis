import sys
sys.path.append('strategies')
import macd
from datetime import date, timedelta

macddd = macd.MACD("DGAZ", (date.today() - timedelta(days = 200)), (date.today() - timedelta(days = 0)))
macddd.plot()
for day in range(0, 50):
    print day
    macdd = macd.MACD("DGAZ", (date.today() - timedelta(days = day + 200)), (date.today() - timedelta(days = day)))
    macdd.calculate_buying_score()
