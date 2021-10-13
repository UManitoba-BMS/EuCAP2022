"""
Spencer Christie
University of Manitoba
July 26th, 2021
"""


import os

import numpy as np

# TODO: Redo comments


def load_session_md(session_dir):
    # Function which loads session metadata from it's directory. A 'key
    # array' is just a text document named "expt_info_key.txt" that
    # has a list of strings ordered in a column.
    # Parameters:
    # key_dir: string of directory that holds the key (should just be a
    # text document).

    key_array = \
        np.genfromtxt(fname=os.path.join(session_dir, "expt_info_key.txt"),
                      dtype='str', delimiter=',')

    return key_array


def load_session_fd(n_expts, session_dir):
    # Function which loads the file directories for all files titled
    # "expt_.txt" in a specified info_directory. Returns these file
    # directories as an array.
    # Parameters:
    # nmber_of_expts: Integer. The number of experiments in the
    # specified info_dir.
    # info_dir: String. Directory in which the experiments are in.

    data_file_arr = np.array([])
    fd_data = np.zeros([n_expts, ])

    for ii in range(n_expts):

        if ii < 10:

            expt_nmbr = "0" + str(ii + 1)

        else:

            expt_nmbr = str(ii + 1)

        data_file_dir = os.path.join(session_dir, "expt%s.txt" % expt_nmbr)
        data_file_arr = np.append(arr=data_file_arr, values=data_file_dir)

    return data_file_arr
