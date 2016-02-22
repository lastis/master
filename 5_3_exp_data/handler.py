import urllib

URL_SPIKE_DATA = 'http://folk.uio.no/danielmb/spike_data.h5'
PATH_SPIKE_DATA = 'spike_data.h5'

def download_data():
    opener = urllib.URLopener()
    print "Downloading: " + URL_SPIKE_DATA
    opener.retrieve(URL_SPIKE_DATA, PATH_SPIKE_DATA)
