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

###############################################################################

__DATA_DIR = os.path.join(get_proj_path(), 'data/20210708-2/')

__OUT_DIR = os.path.join(get_proj_path(), 'output/20210708-2/')
verify_path(__OUT_DIR)

###############################################################################


if __name__ == "__main__":

    fd_data = np.zeros([8, 1001, 72], dtype=complex)
    scan_fs = np.linspace(1e9, 8e9, 1001)
    tar_fs = scan_fs >= 1.65e9

    viridis = get_cmap('magma')

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
        'Plastic 1': td_data[1, :, :],
        'Triton 1': td_data[2, :, :],
        'Adipose 2': td_data[3, :, :],
        'Plastic 2': td_data[4, :, :],
        'Triton 2': td_data[5, :, :],
        'Adipose 3': td_data[6, :, :],
        'Adipose 4': td_data[7, :, :],
    }

    plt_order = [
        'Triton 1',
        'Plastic 1',
        # 'Adipose 2',
        'Adipose 3',
        'Adipose 4'
    ]

    plt_cols = [
        viridis(0),
        viridis(0.3),
        viridis(0.6),
        viridis(0.9),
        viridis(0.9)
    ]

    ###########################################################################

    #
    ref_td = expt_data['Adipose 1']
    tri_td = expt_data['Triton 1']
    cal_tri = np.abs(tri_td - ref_td)
    roi = cal_tri >= 0.75 * np.max(cal_tri)

    plt.figure()
    plt.rc('font', family='Times New Roman')
    plt.tick_params(labelsize=18)

    for ii in range(len(plt_order)):
        tar_str = plt_order[ii]
        tar_td = expt_data[tar_str]

        pix_in_roi = np.abs(tar_td - ref_td)[roi]

        sns.distplot(pix_in_roi, color=plt_cols[ii], label=tar_str)

        s_mean = np.mean(pix_in_roi)
        s_std = np.std(pix_in_roi)
        #
        # plt.axvline(s_mean, color=plt_cols[ii], linestyle='-')
        # plt.axvline(s_mean + s_std, color=plt_cols[ii], linestyle='--')
        # plt.axvline(s_mean - s_std, color=plt_cols[ii], linestyle='--')

    plt.legend(fontsize=16)
    plt.xlabel(r'|S$_{\mathdefault{11}}$|', fontsize=22)
    plt.ylabel("Kernel Density Estimate", fontsize=22)
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(__OUT_DIR, 'kde_plts.png'),
                transparent=False, dpi=300)


    ###########################################################################

    thresholds = np.linspace(0, 1, 100)

    plt.figure(figsize=(9, 6))
    plt.rc('font', family='Times New Roman')
    plt.tick_params(labelsize=18)

    for ii in range(len(plt_order)):
        tar_str = plt_order[ii]
        tar_td = expt_data[tar_str]

        means = np.zeros_like(thresholds)
        stds = np.zeros_like(thresholds)

        for jj in range(len(thresholds)):
            cal_tri = np.abs(tri_td - ref_td)
            roi = cal_tri >= thresholds[jj] * np.max(cal_tri)

            pix_in_roi = np.abs(tar_td - ref_td)[roi]

            means[jj] = np.median(pix_in_roi)
            stds[jj] = np.std(pix_in_roi)

            q75, q25 = np.percentile(pix_in_roi, [75, 25])
            iqr = q75 - q25
            stds[jj] = iqr



        plt.plot(thresholds, means, color=plt_cols[ii], label=plt_order[ii])
        plt.fill_between(thresholds, y1=means - stds,
                         y2=means + stds, color=plt_cols[ii],
                         alpha=0.3)

    plt.legend(fontsize=16)
    plt.xlabel("ROI Threshold", fontsize=22)
    plt.ylabel(r"Median S$_{\mathdefault{11}}$", fontsize=22)
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(__OUT_DIR, 'tys_roi_plt_iqr.png'),
                transparent=False, dpi=300)


