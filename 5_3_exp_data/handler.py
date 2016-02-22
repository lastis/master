import os
import urllib
import neo

URL_SPIKE_DATA = 'http://folk.uio.no/danielmb/spike_data.h5'
PATH_SPIKE_DATA = 'spike_data.h5'

def download_data():
    if not os.path.isfile(PATH_SPIKE_DATA):
        print "Downloading: " + URL_SPIKE_DATA
        urllib.urlretrieve(URL_SPIKE_DATA, PATH_SPIKE_DATA)

    reader = neo.io.NeoHdf5IO(PATH_SPIKE_DATA)
    blocks = reader.read()
    print blocks
