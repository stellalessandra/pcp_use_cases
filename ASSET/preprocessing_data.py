"""
ASSET preprocessing data on fMRI data provided by Jan Schreiber
there are 300 time points (similar to binned spike trains)
for 33865 source locations

"""
import numpy as np
import sys
import neo
import quantities as pq
path_schreiber = '../../ASSET_fMRI/'
activations = np.load(path_schreiber+'activations.npy')
sys.path.append('./ASSET')
import asset

# transform the activations into spike trains
activations_st = []
for item_idx, item in enumerate(activations):
    # take the index of the nonzero elements
    item_st = np.nonzero(item)[0]
    # since there are 300 data points I am assuming that the t_stop is 300s
    item_st = neo.SpikeTrain(item_st,
                             t_start=0*pq.s,
                             t_stop=300*pq.s,
                             units='sec')
    activations_st.append(item_st)

# save the output of the preprocessing
np.save(path_schreiber+'activations_st.npy', activations_st)
