"""
Collection of function to setup necessary files.
"""

import os
import urllib
import neo

URL_SPIKE_DATA = 'http://folk.uio.no/danielmb/spike_data.h5'
PATH_SPIKE_DATA = 'spike_data.h5'


def download_data():
    """
    Download experimental data files.
    """
    if not os.path.isfile(PATH_SPIKE_DATA):
        print "Downloading: " + URL_SPIKE_DATA
        urllib.urlretrieve(URL_SPIKE_DATA, PATH_SPIKE_DATA)


def get_data():
    """
    Return neo blocks.

    Can be iterated with for loop returning a block.
    """
    reader = neo.io.NeoHdf5IO(PATH_SPIKE_DATA)
    blocks = reader.read()
    return blocks
