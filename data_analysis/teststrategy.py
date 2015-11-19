import sys
sys.path.append('strategies')
import macd, vol
from datetime import date, timedelta

test = vol.VOL("AAPL",(date.today() - timedelta(days = 200)), (date.today() - timedelta(days = 0)))
print(test.vol)
test.plot()