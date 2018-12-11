"""
Module utils to reorganize folders
"""

import os
for i in range(1000, 80500, 500):
    directory = '../../ASSET_fMRI/n_channels_%i' % i
    if not os.path.isdir(directory):
        os.mkdir(directory)
    if os.path.exists('../../ASSET_fMRI/sse%i.npy' % i):
        os.rename('../../ASSET_fMRI/sse%i.npy' % i,
                  directory + '/sse%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/mask%i.npy' % i):
        os.rename('../../ASSET_fMRI/mask%i.npy' % i,
                  directory + '/mask%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/xedges%i.npy' % i):
        os.rename('../../ASSET_fMRI/xedges%i.npy' % i,
                  directory + '/xedges%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/yedges%i.npy' % i):
        os.rename('../../ASSET_fMRI/yedges%i.npy' % i,
                  directory + '/yedges%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/imat%i.npy' % i):
        os.rename('../../ASSET_fMRI/imat%i.npy' % i,
                  directory + '/imat%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/pmat%i.npy' % i):
        os.rename('../../ASSET_fMRI/pmat%i.npy' % i,
                  directory + '/pmat%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/jmat%i.npy' % i):
        os.rename('../../ASSET_fMRI/jmat%i.npy' % i,
                  directory + '/imat%i.npy' % i)
    if os.path.exists('../../ASSET_fMRI/cmat%i.npy' % i):
        os.rename('../../ASSET_fMRI/cmat%i.npy' % i,
                  directory + '/cmat%i.npy' % i)
