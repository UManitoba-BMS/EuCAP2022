"""
Tyson Reimer
University of Manitoba
September 28th, 2021
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import seaborn as sns
from scipy import stats

from umbms import get_proj_path, verify_path

from umbms.loadsave import load_birrs_txt
from umbms.sigproc import iczt
from umbms.plot.sinogramplot import plot_sino

###############################################################################

__DATA_DIR = os.path.join(get_proj_path(), 'data/20210617-1/')

__OUT_DIR = os.path.join(get_proj_path(), 'output/20210617-1/')
verify_path(__OUT_DIR)

###############################################################################


if __name__ == "__main__":

    fd_data = np.zeros([8, 1001, 72], dtype=complex)
    scan_fs = np.linspace(1e9, 8e9, 1001)
    tar_fs = scan_fs >= 1.65e9

    viridis = get_cmap('viridis')

    for ii in range(1, 9):
        fd_data[ii - 1, :, :] = load_birrs_txt(os.path.join(__DATA_DIR,
                                                            'expt0%d.txt'
                                                            % ii))
    td_data = np.zeros([8, 700, 72], dtype=complex)
    for ii in range(8):
        fd_here = fd_data[ii, tar_fs, :]
        td_data[ii, :, :] = iczt(fd_data=fd_here,
                                 ini_t=0.5e-9, fin_t=5.5e-9,
                                 ini_f=np.min(scan_fs[tar_fs]),
                                 fin_f=8e9, n_time_pts=700)

    expt_data = {
        'Adipose 1': td_data[0, : ,:],
        'Adipose 2': td_data[1, :, :],
        'Plastic 1': td_data[2, :, :],
        'Triton 1': td_data[3, :, :],
        'Adipose 3': td_data[4, :, :],
        'Plastic 2': td_data[5, :, :],
        'Triton 2': td_data[6, :, :],
        'Adipose 4': td_data[7, :, :],
    }

    threshold = 0.5

    ref_td = expt_data['Adipose 1']
    tri_td = expt_data['Triton 1']

    tar_sino = np.abs(tri_td - ref_td)
    roi = tar_sino >= threshold * np.max(tar_sino)
    crop_sino = tar_sino * np.ones_like(tar_sino)
    crop_sino[~roi] = 0

    plot_sino(td_data=tar_sino,
              ini_t=0.5e-9, fin_t=5.5e-9,
              save_fig=True,
              save_str=os.path.join(__OUT_DIR, 'tri_sino.png'),
              dpi=300,
              transparent=False,
              close_save=False)

    plot_sino(td_data=crop_sino,
              ini_t=0.5e-9, fin_t=5.5e-9,
              save_fig=True,
              transparent=False,
              save_str=os.path.join(__OUT_DIR, 'crop_tri_sino.png'),
              dpi=300,
              close_save=False)



