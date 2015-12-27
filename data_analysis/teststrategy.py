import sys
sys.path.append('strategies')
import macd
from datetime import date, timedelta

macddd = macd.MACD("CMG")
macddd.generate_features()
macddd.train(100)
macddd.predict(100)
# macddd.plot()
