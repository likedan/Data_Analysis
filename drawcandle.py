import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter, WeekdayLocator,\
    DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc

def show_doji(quotes, ax, data, name):
	for index in data:
		ax.text(quotes[index][0], quotes[index][1], name)

def show_doji_test_result(quotes, ax, data, name):
	for index in data[0]:
		ax.text(quotes[index][0], quotes[index][1], name, color='blue')
	for index in data[1]:
		ax.text(quotes[index][0], quotes[index][1], name, color='red')

def draw_candle_stick(stock_id, start_date, end_date, additional_function, data, name):

	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12

	quotes = quotes_historical_yahoo_ohlc(stock_id, start_date, end_date)

	#(?,open,high,low,close,vol)

	if len(quotes) == 0:
	    raise SystemExit

	fig, ax = plt.subplots()
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)

	if additional_function != None:
		additional_function(quotes, ax, data, name)
	#plot_day_summary(ax, quotes, ticksize=3)
	candlestick_ohlc(ax, quotes, width=0.6)

	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')

	# fig.savefig('picture/img.png')   # save the figure to file
	# plt.close(fig)

	plt.show()

