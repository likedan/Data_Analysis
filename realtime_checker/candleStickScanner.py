import helper

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
		if min(low[index - trace_index: index]) >= low[index] and min(closing[index - trace_index: index]) >= closing[index] and vol[index] > vol_ratio * sum(vol[index - trace_index: index - 1]) / trace_index and closing[index] < opening[index]:
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
				lhw_arr[remove] = 0
				remove -= 1
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


