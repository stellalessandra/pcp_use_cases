"""
ASSET test on fMRI data provided by Jan Schreiber
there are 300 time points (similar to binned spike trains)
for 33865 source locations

"""

import numpy as np
import sys
import neo
import quantities as pq
path_schreiber = '../ASSET_fMRI/'
sys.path.append('./ASSET/')
import asset

# remember then to bin the data with 1s binsize
# asset analysis according to the tutorial in asset's page

# data preprocessing in preprocessing_data.py file
sts = np.load('../ASSET_fMRI/activations_st.npy')
# take only the first N channels
number_of_channels = 10
sts = sts[0:number_of_channels]


# 1) Build the intersection matrix `imat` (optional) and the associated
#    probability matrix `pmat` with the desired bin size:

binsize = 1 * pq.s
dt = 300 * pq.s
imat, xedges, yedges = asset.intersection_matrix(sts, binsize, dt, norm=2)
np.save('../ASSET_fMRI/imat%i.npy' % number_of_channels, imat)
np.save('../ASSET_fMRI/xedges%i.npy' % number_of_channels, xedges)
np.save('../ASSET_fMRI/yedges%i.npy' % number_of_channels, yedges)

imat = np.load('../ASSET_fMRI/imat%i.npy' % number_of_channels)
xedges = np.load('../ASSET_fMRI/xedges%i.npy' % number_of_channels)
yedges = np.load('../ASSET_fMRI/yedges%i.npy' % number_of_channels)

pmat, xedges, yedges = asset.probability_matrix_analytical(spiketrains=sts,
                                                           binsize=binsize,
                                                           dt=dt,
                                                           kernel_width=1*pq.s)
np.save('../ASSET_fMRI/pmat%i.npy' % number_of_channels, pmat)
pmat = np.load('../ASSET_fMRI/pmat%i.npy' % number_of_channels)

# 2) Compute the joint probability matrix jmat, using a suitable filter:

filter_shape = (5,2)  # filter shape
nr_neigh = 5  # nr of largest neighbors
jmat = asset.joint_probability_matrix(pmat, filter_shape, nr_neigh)
np.save('../ASSET_fMRI/jmat%i.npy' % number_of_channels, jmat)
jmat = np.load('../ASSET_fMRI/jmat%i.npy' % number_of_channels)


# 3) Create from pmat and jmat a masked version of the intersection matrix:

alpha1 = 0.99
alpha2 = 0.99999
mask = asset.mask_matrices([pmat, jmat], [alpha1, alpha2])
np.save('../ASSET_fMRI/mask%i.npy' % number_of_channels, mask)
mask = np.load('../ASSET_fMRI/mask%i.npy' % number_of_channels)

# 4) Cluster significant elements of imat into diagonal structures ("DSs"):

epsilon = 10
minsize = 2
stretch = 2

cmat = asset.cluster_matrix_entries(mask, epsilon, minsize, stretch)
np.save('../ASSET_fMRI/cmat%i.npy' % number_of_channels, cmat)
mask = np.load('../ASSET_fMRI/cmat%i.npy' % number_of_channels)

# 5) Extract sequences of synchronous events associated to each worm

sse = asset.extract_sse(sts, xedges, yedges, cmat)
np.save('../ASSET_fMRI/sse%i.npy' % number_of_channels, sse)
