import os

from utils.preprocessing import get_centered_sample
from settings import WINDOW
from settings import MUSIC_SAMPLE_RATE as SR
import numpy as np


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))



def full_song_output(md, src):
    if len(src.shape) == 1:
        src = src[np.newaxis, :]
    n = src.shape[1]
    trunc_size = 5
    min_ind = trunc_size * SR
    max_ind = n - ((5 + WINDOW) * SR)
    interv = (max_ind - min_ind) + WINDOW * SR
    interv_s = int(interv / SR)
    OVERLAP = 0

    if interv_s < (2 * WINDOW - OVERLAP) + 1:  # case of short sample
        return centered_song_output(md, src)
    else:
        n_samples = int((interv_s - OVERLAP) // (WINDOW - OVERLAP)) - 1
        sub_srcs = np.empty((n_samples, 1, WINDOW * SR), dtype=float)

        for i in range(n_samples):
            if i == n_samples - 1:
                offset = max_ind
            else:
                offset = min_ind + i * (WINDOW - OVERLAP) * SR
            sub_src = src[..., offset:offset + WINDOW * SR]
            sub_srcs[i, ...] = sub_src

        outputs = md.predict(sub_srcs)
        return np.mean(np.asarray(outputs), axis=0)



def mean_song_output(md,src):
    return full_song_output(md,src,)

def centered_song_output(md,src):
    src = get_centered_sample(src)
    src = src[np.newaxis, :]
    if src.shape!=(1,1,348000):
        res = np.zeros((1,1,348000))
        res[0,0,:src.shape[2]] = src
        src = res
    return md.predict(src)

if __name__=='__main__':
    pass
