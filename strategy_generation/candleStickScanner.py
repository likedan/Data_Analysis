import helper

def scan_doji(opening, closing, high, low):
	ratio_factor = 0.15
	doji_arr = []
	doji_index = []
	if not (len(opening) == len(closing) == len(high) == len(low)):
		raise Exception('scan_doji input inconsistent length') 
	for index in xrange(len(opening)):
		if abs(opening[index] - closing[index]) < abs(high[index] - low[index]) * ratio_factor:
			doji_arr.append(1)
			doji_index.append(index)
		else:
			doji_arr.append(0)
	return (doji_arr, doji_index)


def scan_dragonfly_doji(opening, closing, high, low, doji_arr):
	ratio_factor = 0.2
	dragonfly_doji_arr = doji_arr
	dragonfly_doji_index = []
	if not (len(opening) == len(closing) == len(high) == len(low) == len(doji_arr)):
		raise Exception('scan_dragonfly_doji input inconsistent length') 
	for index in xrange(len(doji_arr)):
		if doji_arr[index] == 1:
			if closing[index] > abs(high[index] - low[index]) * (1 - ratio_factor) + low[index] and opening[index] > abs(high[index] - low[index]) * (1 - ratio_factor) + low[index]:
				dragonfly_doji_index.append(index)
			else:
				dragonfly_doji_arr[index] = 0
	return (dragonfly_doji_arr, dragonfly_doji_index)


def scan_gravestone_doji(opening, closing, high, low, doji_arr):
	ratio_factor = 0.2
	gravestone_doji_arr = doji_arr
	gravestone_doji_index = []
	if not (len(opening) == len(closing) == len(high) == len(low) == len(doji_arr)):
		raise Exception('scan_gravestone_doji input inconsistent length') 
	for index in xrange(len(doji_arr)):
		if doji_arr[index] == 1:
			if closing[index] < abs(high[index] - low[index]) * ratio_factor + low[index] and opening[index] < abs(high[index] - low[index]) * ratio_factor + low[index]:
				gravestone_doji_index.append(index)
			else:
				gravestone_doji_arr[index] = 0
	return (gravestone_doji_arr, gravestone_doji_index)


def scan_stars(opening, closing, high, low, is_bullish):

	#first two unidentifiable

	star_arr = [0, 0]
	star_index = []
	if not (len(opening) == len(closing) == len(high) == len(low)):
		raise Exception('scan_stars input inconsistent length')

	#index of the 3rd bar 
	for index in xrange(2, len(opening)):

		middle_index = index - 1

		# 1st and 3rd   valid trend   greater than average movement
		def is_valid_trend():
			am_frame = 10
			ratio_factor = 0.75
			start = middle_index - am_frame
			end = middle_index + am_frame
			if start < 0:
				start = 0
			if end >= len(opening):
				end = len(opening) - 1

			average_movement = helper.get_average_movement(opening[start:end], closing[start:end])
			if abs(closing[middle_index - 1] - opening[middle_index - 1]) < average_movement * ratio_factor:
				return False
			if abs(closing[middle_index + 1] - opening[middle_index + 1]) < average_movement * ratio_factor:
				return False
			if abs(closing[middle_index] - opening[middle_index]) > average_movement:
				return False
			return True

		if not is_valid_trend():
			star_arr.append(0)
			continue

		if is_bullish:
			# no overlap
			if opening[middle_index + 1] > closing[middle_index] and closing[middle_index - 1] > closing[middle_index]:

				# 2 bars valid direction
				if opening[middle_index - 1] > closing[middle_index - 1] and opening[middle_index + 1] < closing[middle_index + 1]:
					star_arr.append(1)
					star_index.append(index)
				else:
					star_arr.append(0)
			else:
				star_arr.append(0)
		else:
			# no overlap
			if opening[middle_index + 1] < opening[middle_index] and closing[middle_index - 1] < opening[middle_index]:

				# 2 bars valid direction
				if opening[middle_index - 1] < closing[middle_index - 1] and opening[middle_index + 1] > closing[middle_index + 1]:
					star_arr.append(1)
					star_index.append(index)
				else:
					star_arr.append(0)
			else:
				star_arr.append(0)

	return (star_arr, star_index)

def scan_hammer(opening, closing, high, low):
	head_ratio = 0.125
	length_ratio = 0.4
	hammer_arr = []
	hammer_index = []
	if not (len(opening) == len(closing) == len(high) == len(low)):
		raise Exception('scan_hammer input inconsistent length') 

	for index in xrange(len(opening)):
		length = high[index] - low[index]
		if opening[index] < low[index] + length_ratio * length and closing[index] < low[index] + length_ratio * length:
			#inverted hammer
			if opening[index] < low[index] + head_ratio * length or closing[index] < low[index] + head_ratio * length:
				hammer_arr.append(1)
				hammer_index.append(index)
			else:
				hammer_arr.append(0)
		elif opening[index] > low[index] + (1 - length_ratio) * length and closing[index] > low[index] + (1 - length_ratio) * length:
			#hammer
			if opening[index] > low[index] + (1 - head_ratio) * length or closing[index] > low[index] + (1 - head_ratio) * length:
				hammer_arr.append(1)
				hammer_index.append(index)
			else:
				hammer_arr.append(0)
		else:
			hammer_arr.append(0)

	return (hammer_arr, hammer_index)


def scan_bullish_hammer(opening, closing, high, low, hammer_arr, is_inverted = None):

	inverted_hammer_arr = hammer_arr
	inverted_hammer_index = []
	if not (len(opening) == len(closing) == len(high) == len(low) == len(hammer_arr)):
		raise Exception('scan_hammer input inconsistent length') 
	
		#first unidentifiable
	inverted_hammer_arr[0] = 0
	inverted_hammer_arr[1] = 0

	for index in xrange(2, len(hammer_arr)):
		if hammer_arr[index] == 1:
			#valid downtrend
			if not (closing[index - 1] < opening[index - 1] and closing[index - 2] < opening[index - 2] and closing[index - 2] > closing[index - 1]):
				inverted_hammer_arr[index] = 0
				continue

			length = high[index] - low[index]

			if is_inverted != None:
				if is_inverted:
					if closing[index] < low[index] + 0.5 * length and opening[index] < low[index] + 0.5 * length:
						inverted_hammer_arr[index] = 1
						inverted_hammer_index.append(index)
					else:
						inverted_hammer_arr[index] = 0
				else:
					if closing[index] > low[index] + 0.5 * length and opening[index] > low[index] + 0.5 * length:
						inverted_hammer_arr[index] = 1
						inverted_hammer_index.append(index)
					else:
						inverted_hammer_arr[index] = 0
			else:
				inverted_hammer_arr[index] = 1
				inverted_hammer_index.append(index)

	return (inverted_hammer_arr, inverted_hammer_index)

def scan_three_line_strike(opening, closing, high, low):

	strike_arr = []
	strike_index = []
	if not (len(opening) == len(closing) == len(high) == len(low)):
		raise Exception('scan_hammer input inconsistent length') 
	
	#first unidentifiable
	for index in xrange(3):
		strike_arr.append(0)

	for index in xrange(3, len(opening)):
		#valid downtrend
		valid_trend = True
		for prev in xrange(3):
			if closing[index - 3 + prev] > opening[index - 3 + prev]:
				valid_trend = False

		for prev in xrange(2):
			if closing[index - 3 + prev] < closing[index - 2 + prev]:
				valid_trend = False

		if opening[index] > closing[index - 1]:
			valid_trend = False
		if closing[index] < opening[index - 3]:
			valid_trend = False	
			
		if valid_trend:
			strike_arr.append(1)
			strike_index.append(index)
		else:
			strike_arr.append(0)

	return (strike_arr, strike_index)


def scan_bullish_harami(opening, closing, high, low):

	harami_arr = []
	harami_index = []
	if not (len(opening) == len(closing) == len(high) == len(low)):
		raise Exception('scan_hammer input inconsistent length') 
	
	#first unidentifiable
	harami_arr.append(0)
	harami_arr.append(0)
	harami_arr.append(0)

	for index in xrange(3, len(opening)):
		if closing[index - 2] < closing[index - 3] and closing[index - 1] < closing[index - 2] and opening[index] < closing[index] and opening[index - 1] > closing[index - 1] and closing[index] < opening[index - 1] and opening[index] > closing[index - 1] and high[index] < high[index - 1] and low[index] > low[index - 1]:
			harami_arr.append(1)
			harami_index.append(index)
		else:
			harami_arr.append(0)

	return (harami_arr, harami_index)


def scan_low_with_huge_vol(opening, closing, high, low, vol):

	lhw_arr = []
	lhw_index = []
	if not (len(opening) == len(closing) == len(high) == len(low) == len(vol)):
		raise Exception('scan_hammer input inconsistent length') 

	trace_index = 15	
	#first unidentifiable
	for index in xrange(trace_index):
		lhw_arr.append(0)

	vol_ratio = 1.5
	for index in xrange(trace_index, len(opening)):
		#new low with big vol
		if min(low[index - trace_index: index]) >= low[index] and min(closing[index - trace_index: index]) >= closing[index] and vol[index] > vol_ratio * sum(vol[index - trace_index: index - 1]) / trace_index and closing[index] < opening[index]: # and sum(vol[index - trace_index: index - 1]) / trace_index > 200000:
			lhw_arr.append(1)
			lhw_index.append(index)
		else:
			lhw_arr.append(0)		

	return (lhw_arr, lhw_index)

def scan_low_with_huge_vol_consecutive(opening, closing, lhw_arr, separate_by_price_moving_range = False):
	lhw_index = []
	for index in reversed(xrange(1, len(lhw_arr))):
		if lhw_arr[index] == 1 and lhw_arr[index - 1] == 1:
			lhw_index.append(index)
			remove = index - 1
			while lhw_arr[remove] == 1 and remove >= 0:
				remove -= 1
			lhw_arr[remove + 1] = 0
		else:
			lhw_arr[index] = 0

	if separate_by_price_moving_range:
		temp_lhw_index = []
		length_ratio = 1.8
		for index in lhw_index:

			am_frame = 10
			start = index - am_frame
			if start < 0:
				start = 0

			average_movement = helper.get_average_movement(opening[start: index], closing[start: index])
			if abs(closing[index] - opening[index]) < average_movement * length_ratio:
				#wrong
				lhw_arr[index] = 0
			else:
				temp_lhw_index.append(index)

		lhw_index = temp_lhw_index

	return (lhw_arr, lhw_index)

def scan_low_with_huge_vol_consecutive_three(opening, closing, lhw_arr, separate_by_price_moving_range = False):
	lhw_index = []
	for index in reversed(xrange(2, len(lhw_arr))):
		if closing[index] < closing[index - 1] and opening[index] > closing[index] and lhw_arr[index - 1] == 1 and lhw_arr[index - 2] == 1:
			lhw_index.append(index)
			remove = index - 1
			while lhw_arr[remove] == 1 and remove >= 0:
				lhw_arr[remove] = 0
				remove -= 1
		else:
			lhw_arr[index] = 0

	if separate_by_price_moving_range:
		temp_lhw_index = []

		for index in lhw_index:

			am_frame = 10
			start = index - am_frame
			if start < 0:
				start = 0

			average_movement = helper.get_average_movement(opening[start: index], closing[start: index])
			if abs(closing[index] - opening[index]) < average_movement:
				#wrong
				lhw_arr[index] = 0
			else:
				temp_lhw_index.append(index)

		lhw_index = temp_lhw_index

	return (lhw_arr, lhw_index)

def scan_high_moving_range(opening, closing):
	ratio_factor = 1.5
	range_arr = []
	range_index = []
	for index in xrange(len(opening)):

		am_frame = 10
		start = index - am_frame
		if start < 0:
			range_arr.append(0)
			continue

		average_movement = helper.get_average_movement(opening[start: index], closing[start: index])
		if abs(closing[index] - opening[index]) < average_movement * ratio_factor:
			#wrong
			range_arr.append(0)
		else:
			range_arr.append(1)
			range_index.append(index)


	return (range_arr, range_index)

def scan_high_relative_volume(vol):
	ratio_factor = 1.5
	vol_arr = []
	vol_index = []
	for index in xrange(10, len(opening)):
		am_frame = 10
		start = index - am_frame
		if start < 0:
			start = 0

		average = sum(vol[start: index]) / am_frame
		if average * ratio_factor > vol[index]:
			#wrong
			vol_arr.append(0)
		else:
			vol_arr.append(1)
			vol_index.append(index)
	return (vol_arr, vol_index)
