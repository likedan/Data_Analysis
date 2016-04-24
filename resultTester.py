import helper

#determine in the following day after pattern occur, the price went up or down.   based on next day opening and closing    
def test_next_one_day_price(opening, closing, index_arr, should_up, should_above_average_movement):

	positive = []
	negative = []
	if not should_up:
		#swap
		opening, closing = closing, opening

	max_index = max(index_arr)
	if not ((len(opening) == len(closing)) and max_index < len(opening)):
		raise Exception('test_next_one_day_price input inconsistent length') 
	else:
		#remove last redundant
		if max_index + 1 == len(opening):
			index_arr.remove(max_index)

		for index in index_arr:

			if opening[index + 1] < closing[index + 1]:
				if should_above_average_movement:
					am_frame = 10
					start = index - am_frame
					end = index + am_frame
					if start < 0:
						start = 0
					if end >= len(opening):
						end = len(opening) - 1

					average_movement = helper.get_average_movement(opening[start:end], closing[start:end])

					if closing[index + 1] - opening[index + 1] > average_movement:
						positive.append(index)
					else:
						negative.append(index)
				else:
					positive.append(index)
			else:
				negative.append(index)

	return [positive, negative]

#determine in the following day opening price or closing price is higher than today's closing price.   based on today closing next day opening
def test_next_day_opening_and_closing_price(opening, closing, index_arr):

	positive = []
	negative = []

	max_index = max(index_arr)
	if not ((len(opening) == len(closing)) and max_index < len(opening)):
		raise Exception('test_next_day_opening_price input inconsistent length') 
	else:
		#remove last redundant
		if max_index + 1 == len(opening):
			index_arr.remove(max_index)

		for index in index_arr:
			if opening[index + 1] > closing[index] or closing[index + 1] > closing[index]:
				positive.append(index)
			else:
				negative.append(index)
	return [positive, negative]

#determine in the following day opening price is higher than closing price.   based on today closing next day opening
def test_next_day_opening_price(opening, closing, index_arr):

	positive = []
	negative = []

	max_index = max(index_arr)
	if not ((len(opening) == len(closing)) and max_index < len(opening)):
		raise Exception('test_next_day_opening_price input inconsistent length') 
	else:
		#remove last redundant
		if max_index + 1 == len(opening):
			index_arr.remove(max_index)

		for index in index_arr:
			if opening[index + 1] > closing[index]:
				positive.append(index)
			else:
				negative.append(index)
	return [positive, negative]


#determine in the following day closing price is higher than today closing price.   based on today closing and next day closing
def test_next_day_closing_price(closing, index_arr):

	positive = []
	negative = []

	max_index = max(index_arr)
	if not max_index < len(closing):
		raise Exception('test_next_day_closing_price input inconsistent length') 
	else:
		#remove last redundant
		if max_index + 1 == len(closing):
			index_arr.remove(max_index)

		for index in index_arr:
			if closing[index + 1] > closing[index]:
				positive.append(index)
			else:
				negative.append(index)

	return [positive, negative]



