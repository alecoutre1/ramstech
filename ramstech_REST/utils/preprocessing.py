import numpy as np

def get_centered_sample(x):
    if len(x.shape) == 1:
        x = x[np.newaxis, :]
    offset = (x.shape[1] - 348000) // 2
    return x[..., offset:offset + 348000]