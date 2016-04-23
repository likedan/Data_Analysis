import numpy as np

def get_average_movement(opening, closing):
	opening = np.array(opening)
	closing = np.array(closing)
	movement = closing - opening
	abs_movement = np.absolute(movement) 

	return np.sum(abs_movement) / len(opening)