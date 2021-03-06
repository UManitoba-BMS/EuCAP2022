"""
Spencer Christie
University of Manitoba
July 26th, 2021
"""


import os

from pathlib import Path

import numpy as np

import matplotlib.pyplot as plt

from umbms import get_proj_path, verify_path, get_script_logger

from umbms import processdata as procd
from umbms.plot import customplotfuncts as cpf
from umbms.pathing import findpaths as fp

###############################################################################

all_sessions = os.listdir(os.path.join(get_proj_path(), 'data/'))

for session_str in all_sessions:


    __DATA_DIR = os.path.join(get_proj_path(), 'data/%s/' % session_str)

    __OUT_DIR = os.path.join(get_proj_path(), 'output/%s/' % session_str)
    verify_path(__OUT_DIR)

    ###############################################################################

    delete_air = True  # If true, any air scans are deleted
    crop_tri_1 = False  # If true, crop by the 1st triton scan
    crop_tri_2 = False  # if true, crop by the 2nd triton scan
    crop_cutoff = 0.5  # Should be between 0 and 1
    save_figs = True  # if true, saves figures, else shows them to you

    ###############################################################################

    # Load the names and file paths of the scans, which is done via a
    # "key" which is  really just a plain text document in the data
    # directory that has the names of all the scans in an ordered list.
    scan_names = fp.load_session_md(session_dir=__DATA_DIR)
    scan_paths = fp.load_session_fd(n_expts=len(scan_names),
                                    session_dir=__DATA_DIR)

    # The air scan skews the scale, thus the option to delete it
    if delete_air:

        for ii in range(len(scan_names)):  # For each scan

            # If the scan is air, delete it from arr
            if scan_names[ii].startswith("Air"):
                scan_names = np.delete(arr=scan_names, obj=ii)
                scan_paths = np.delete(arr=scan_paths, obj=ii)

    # Set some placeholder values for the cropping variables to
    # avoid warnings:
    cropping = False
    cutoff_str = "Placeholder"
    crop_name = "Placeholder"
    crop_scan = 5

    # If we want to crop the image with respect to either of the
    # triton scans, first we need to find the triton scan and save it's
    # data for later. Note that if both crop_tri_1 and crop_tri_2 are True,
    # crop_tri_1 will take priority.
    if crop_tri_1:

        for ii in range(len(scan_names)):

            if scan_names[ii].startswith("Triton 1"):
                crop_scan = scan_paths[ii]
                crop_name = scan_names[ii]
                cropping = True
                cutoff_str = "{:.2f}".format(crop_cutoff)
                print("Cropping by %s." % crop_name)

    elif crop_tri_2:

        for ii in range(len(scan_names)):

            if scan_names[ii].startswith("Triton 2"):
                crop_scan = scan_paths[ii]
                crop_name = scan_names[ii]
                cropping = True
                cutoff_str = "{:.2f}".format(crop_cutoff)
                print("Cropping by %s." % crop_name)

    # If we want to crop by triton 1 or 2, but cropping is still false after
    # checking all scan_names (which means we couldn't find the triton
    # scan), except.
    if (crop_tri_1 or crop_tri_2) and not cropping:
        raise Exception("Triton 1 or 2 wasn't found to crop! Check data.")

    # Named constants for the ICZT transform.
    ini_t = 0.5e-9  # In seconds
    fin_t = 5.5e-9  # In seconds
    n_t_pts = 700
    ini_f = 1e9  # In hz
    fin_f = 8e9  # In hz

    # Any frequencies below this cutoff_freq are removed before we convert
    # to the time domain.
    cutoff_freq = 1.65e9  # In hz

    # Need to get the size and shape of the array generated by
    # the BIRRS software. So create a test data array:
    test_array, new_i_freq = procd.get_cut_td(data_path=scan_paths[0],
                                              c_data_path=scan_paths[1],
                                              i_time=ini_t, f_time=fin_t,
                                              time_pnts=n_t_pts,
                                              i_freq=ini_f, f_freq=fin_f,
                                              freq_cut=cutoff_freq, show_cut=True)
    row_amount, column_amount = test_array.shape
    print("Number of rows is %s and number of columns is %s"
          % (row_amount, column_amount))

    # For each scan...
    for ii in range(len(scan_names)):

        # The loop iterates over all scans, but we actually only want to
        # iterate over all reference (adipose/air) scans. So skip the loop
        # if it is not an adipose/air scan:
        if not (scan_names[ii].startswith("Adipose")
                or scan_names[ii].startswith("Air")):
            continue

        # Get the reference scan:
        ref_scan_path = scan_paths[ii]
        ref_scan_name = scan_names[ii]
        print("%s is currently the reference." % scan_names[ii])

        # Make local numpy lists where the reference scan is deleted.
        # The reference is subtracted from all scans, so it itself cannot
        # be shown whilst being used as a reference.
        new_scan_names = np.delete(arr=scan_names, obj=ii)
        new_scan_paths = np.delete(arr=scan_paths, obj=ii)
        new_scan_data = np.zeros(shape=(len(new_scan_paths), row_amount,
                                        column_amount))

        if cropping:
            crop_array = procd.get_cut_td(data_path=crop_scan,
                                          c_data_path=ref_scan_path,
                                          i_time=ini_t, f_time=fin_t,
                                          time_pnts=n_t_pts,
                                          i_freq=ini_f, f_freq=fin_f,
                                          freq_cut=cutoff_freq)

        else:
            crop_array = None

        # For each of the new_scan_paths (AKA all scans but the reference):
        for jj in range(len(new_scan_paths)):
            # Get the data for that scan:
            new_scan_data[jj] = procd.get_cut_td(data_path=new_scan_paths[jj],
                                                 c_data_path=ref_scan_path,
                                                 i_time=ini_t,
                                                 f_time=fin_t,
                                                 time_pnts=n_t_pts,
                                                 i_freq=ini_f,
                                                 f_freq=fin_f,
                                                 freq_cut=cutoff_freq)
            print("%s data was just obtained." % new_scan_names[jj])

        # Now that we have the data...

        # If we want to filter it in terms of a roi, do that.
        if cropping:

            for jj in range(len(new_scan_paths)):
                new_scan_data[jj] = procd.get_roi_2d(array=new_scan_data[jj],
                                                     roi_array=crop_array,
                                                     cutoff=crop_cutoff)

        # Define some variables for the plot:
        cbar_txt = "Magnitude of $\\mathdefault{S_{11}}$ Response"
        max_scatter = np.amax(new_scan_data)
        min_scatter = np.amin(new_scan_data)

        # Need to get the actual initial frequency.
        starting_freq = new_i_freq

        # For each scan except the reference...
        for jj in range(len(new_scan_paths)):

            title = "%s with respect \n to %s" % (new_scan_names[jj],
                                                  ref_scan_name)
            cbar = cpf.plot_sino_birrs(input_data=new_scan_data[jj],
                                       title=title, norm_value=max_scatter,
                                       start_time=ini_t,
                                       cbar_label=cbar_txt, stop_time=fin_t)

            if save_figs:

                print("Saving sinograms calibrated with respect to %s..."
                      % ref_scan_name)

                # The file name will change depending on what parameters
                # are set to true at the beginning of the file.
                path_name = __OUT_DIR + "\\" + new_scan_names[jj] + "_WRT_" \
                            + ref_scan_name

                if cropping:
                    path_name += "_" + crop_name + "_" + cutoff_str

                path_name += ".png"
                plt.savefig(fname=path_name, dpi=300, transparent=False)
                cbar.remove()
                plt.clf()

            # If we don't want to save the figure, show it instead.
            else:
                plt.show()
