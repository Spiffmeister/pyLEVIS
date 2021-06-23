'''
    GET THE SCENIC.IN DATA
'''

import os
import re


def Get_ScenicData(LEVIS):
    fname = os.path.join(LEVIS.mercurydir,"scenic.in")

    try:
        f_open = open(fname)
        keys_data_float = ["antenna_power","toroidal_mode","power_partition","icrh_nr","icrh_nz","icrh_nphi","splitting_factor","density_avg","coarse_grain_bin","charge_majority","mass_majority","Zeff","charge_ratio","mass_ratio"]

        data = dict()

        for line in f_open:
            for key in keys_data_float:
                if key in line:
                    add = re.split("=|!",line)
                    data[key] = float(add[1])
        f_open.close()

    except:
        raise FileNotFoundError('No scenic.in file found in {}'.format(LEVIS.mercurydir))

    return data
