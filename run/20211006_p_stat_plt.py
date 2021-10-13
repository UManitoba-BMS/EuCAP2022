"""
Tyson Reimer
University of Manitoba
October 06th, 2021
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap

from umbms import get_proj_path, verify_path
from umbms.loadsave import load_pickle

###############################################################################

__DIR_1 = os.path.join(get_proj_path(), 'output/20210708-2/')
__DIR_2 = os.path.join(get_proj_path(), 'output/20210617-1/')

__OUT_DIR = os.path.join(get_proj_path(), 'output/')

###############################################################################

if __name__ == "__main__":

    cutoffs_1, ps_1 = load_pickle(os.path.join(__DIR_1,
                                               'Ref_of_Adipose 1_cropped_by_Triton 1_700_time_points.pickle'))

    cutoffs_2, ps_2 = load_pickle(os.path.join(__DIR_2,
                                               'Ref_of_Adipose 1_cropped_by_Triton 1_700_time_points.pickle'))

    cmap = get_cmap('magma')

    plt.figure(figsize=(10, 8))
    plt.rc('font', family='Times New Roman')
    plt.tick_params(labelsize=18)
    plt.plot(cutoffs_2, ps_2, color=cmap(0.5), linestyle='-',
             label='Median Overlap Example')
    plt.plot(cutoffs_1, ps_1, color=cmap(0), linestyle='--',
             label='No Median Overlap Example')

    plt.legend(fontsize=20)
    plt.xlabel('ROI Threshold Value', fontsize=22)
    plt.ylabel('P-Value', fontsize=22)
    # plt.yscale('log')
    plt.tight_layout()
    plt.show()
    plt.savefig(os.path.join(__OUT_DIR, 'p_plt_fig.png'),
                transparent=False,
                dpi=300)