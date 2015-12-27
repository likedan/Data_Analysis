import sys
sys.path.append('strategies')
import macd
from datetime import date, timedelta

macddd = macd.MACD("AAPL")
# macddd.generate_features()
macddd.train(20)
macddd.predict(20)
# macddd.plot()
