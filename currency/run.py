db = Database()
currency_data = db.get_range_currency_date("EURUSD", 20160416 ,20160606)
for day_data in currency_data:
	frame, resistance_lines, support_lines = compute_support_resistance(day_data,frame_size = 80)

	good_support = []
	for l in reversed(support_lines[-7:]):
		good_support.append(l["line"])
		print l
	good_resisitance = []
	for l in reversed(resistance_lines[-7:]):
		good_resisitance.append(l["line"])
		print l
	good_lines = []
	for index in range(len(good_resisitance)):
		good_lines.append([good_support[index],good_resisitance[index]])

	Plot.plot_day_candle(frame, day_data["unix_time"], "EURUSD", lines=good_lines, save=True)