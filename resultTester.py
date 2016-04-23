
#determine in the following day after pattern occur, the price went up or down.   based on next day opening and closing
def test_next_one_day_price(opening, closing, index_arr, average_movement, is_up):

	positive = 0
	negative = 0

	if not is_up:
		#swap
		opening, closing = closing, opening

	max_index = max(index_arr)
	if not ((len(opening) == len(closing)) and max_index < len(opening)):
		raise Exception('scan_dragonfly_doji input inconsistent length') 
	else:
		#remove last redundant
		if max_index + 1 == len(opening):
			index_arr.remove(max_index)

		for index in index_arr:
			if opening[index + 1] < closing[index + 1] and closing[index + 1] - opening[index + 1] > average_movement:
				positive += 1
			else:
				negative += 1

	return [positive, negative]
