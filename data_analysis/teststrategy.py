import sys
sys.path.append('strategies')
import macd, vol
from datetime import date, timedelta

test = vol.VOL("GOOG",(date.today() - timedelta(days = 200)), (date.today() - timedelta(days = 0)))
print(test.calculate_vol())