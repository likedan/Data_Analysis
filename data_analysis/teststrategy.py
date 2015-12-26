import sys
sys.path.append('strategies')
import macd
from datetime import date, timedelta

macddd = macd.MACD("UWTI",200)
macddd.generate_features()
macddd.plot()
