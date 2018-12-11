"""
SPADE test on fMRI data provided by Jan Schreiber
there are 300 time points (similar to binned spike trains)
for 33865 source locations

"""

import numpy as np
import sys
import neo
import quantities as pq
path_schreiber = '../ASSET_fMRI/'
sys.path.append('./ASSET/')
import elephant.spade as spade

# remember then to bin the data with 1s binsize

# data preprocessing in preprocessing_data.py file
sts = np.load('../ASSET_fMRI/activations_st.npy')
# take only the first N channels
number_of_channels = 100
sts = sts[0:number_of_channels]

# spade parameters
binsize = 1 * pq.s
dt = 300 * pq.s
winlen = 60
min_occ = 3
min_spikes = 3
min_neu = 3
n_surr = 1000
alpha = 0.05
dither = 0.005
psr_param = [2, 2, 2]
spectrum = '3d#'


spade_res = spade.spade(sts,
                        binsize,
                        winlen,
                        min_occ=min_occ,
                        min_spikes=min_spikes,
                        min_neu=min_neu,
                        dither=dither,
                        n_surr=n_surr,
                        alpha=alpha,
                        psr_param=psr_param,
                        spectrum=spectrum)

np.save('../SPADE_fMRI/spade_res%i.npy' % number_of_channels, spade_res)


