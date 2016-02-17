import numpy as np

dataset = [1,5,2,7,3,34,3,4,6]

def get_moving_average(values, window):
    weights = np.repeat(1.0, window) / window
    print weights
    arr = []
    for value in values:
        print value
        arr.append(int(value * 100))

    smas = np.convolve(values, weights, "valid")
    smas = smas / 100.0
    return smas
    
def get_exp_moving_average(values, window):
    weights = np.exp(np.linspace(-1.0, 0.,window))
    print weights
    weights = weights / weights.sum()
    print weights
    a = np.convolve(values, weights)[:len(values)]
    print a
    a[:window] = a[window]
    return a
    
    
print get_exp_moving_average(dataset, 3)