"""
ASSET test on fMRI data provided by Jan Schreiber
there are 300 time points (similar to binned spike trains)
for 33865 source locations

"""

import numpy as np
import sys
import neo
import quantities as pq
path_fmri = '../ASSET_fMRI/'
sys.path.append('./ASSET/')
import asset

# remember then to bin the data with 1s binsize
# asset analysis according to the tutorial in asset's page

# data preprocessing in preprocessing_data.py file
sts = np.load(path_fmri + 'activations_st.npy')
# take only the first N channels
number_of_channels = 10
sts = sts[0:number_of_channels]

# choose whether you want to calculate the probability matrix analytically
# or via surrogates
# you can choose between 'analytical', 'montecarlo'
analysis_flag = 'analytical'


# 1) Build the intersection matrix `imat` (optional) and the associated
#    probability matrix `pmat` with the desired bin size:

binsize = 1 * pq.s
dt = 300 * pq.s
imat, xedges, yedges = asset.intersection_matrix(sts, binsize, dt, norm=2)
np.save(path_fmri + 'imat%i.npy' % number_of_channels, imat)
np.save(path_fmri + 'xedges%i.npy' % number_of_channels, xedges)
np.save(path_fmri + 'yedges%i.npy' % number_of_channels, yedges)

imat = np.load(path_fmri + 'imat%i.npy' % number_of_channels)
xedges = np.load(path_fmri + 'xedges%i.npy' % number_of_channels)
yedges = np.load(path_fmri + 'yedges%i.npy' % number_of_channels)

if analysis_flag == 'analytical':

    pmat, xedges, yedges = asset.probability_matrix_analytical(spiketrains=sts,
                                                               binsize=binsize,
                                                               dt=dt,
                                                               kernel_width=
                                                               10*pq.s)
    np.save(path_fmri + 'pmat%i.npy' % number_of_channels, pmat)
    pmat = np.load(path_fmri + 'pmat%i.npy' % number_of_channels)

elif analysis_flag == 'montecarlo':
    j = 5 * pq.s
    pmat, xedges, yedges = asset.probability_matrix_montecarlo(spiketrains=sts,
                                                               binsize=binsize,
                                                               dt=dt,
                                                               j=j,
                                                               surr_method=
                                                               'dither_spikes')
    np.save(path_fmri + 'pmat_montecarlo%i.npy' % number_of_channels, pmat)
    pmat = np.load(path_fmri + 'pmat%i.npy' % number_of_channels)
else:
    print('type of analysis must be specified')
    
# 2) Compute the joint probability matrix jmat, using a suitable filter:

filter_shape = (5,2)  # filter shape
nr_neigh = 5  # nr of largest neighbors
jmat = asset.joint_probability_matrix(pmat, filter_shape, nr_neigh)
np.save(path_fmri + 'jmat%i.npy' % number_of_channels, jmat)
jmat = np.load(path_fmri + 'jmat%i.npy' % number_of_channels)


# 3) Create from pmat and jmat a masked version of the intersection matrix:

alpha1 = 0.99
alpha2 = 0.99999
mask = asset.mask_matrices([pmat, jmat], [alpha1, alpha2])
np.save(path_fmri + 'mask%i.npy' % number_of_channels, mask)
mask = np.load(path_fmri + 'mask%i.npy' % number_of_channels)

# 4) Cluster significant elements of imat into diagonal structures ("DSs"):

epsilon = 10
minsize = 2
stretch = 2

cmat = asset.cluster_matrix_entries(mask, epsilon, minsize, stretch)
np.save(path_fmri + 'cmat%i.npy' % number_of_channels, cmat)
mask = np.load(path_fmri + 'cmat%i.npy' % number_of_channels)

# 5) Extract sequences of synchronous events associated to each worm

sse = asset.extract_sse(sts, xedges, yedges, cmat)
np.save(path_fmri + 'sse%i.npy' % number_of_channels, sse)

