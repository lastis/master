# pylint: disable=invalid-name, missing-docstring
import handler
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, lfilter, filtfilt

handler.download_data()
blocks = handler.get_data()

spiketrain = blocks[0].recordingchannelgroups[2].units[4].spiketrains[0]
t_vec = spiketrain.times
signal = spiketrain.waveforms
signal = signal[:,0,0]

print spiketrain.t_stop
print signal[0]

plt.figure()
plt.plot(t_vec, signal)

# sample_freq = spiketrain.sampling_rate
sample_freq = len(t_vec)/t_vec[-1]*1000
print sample_freq
nyq = 0.5 * sample_freq
high = 6700/nyq
low = 300/nyq
b, a = butter(1, [low, high])
signal = lfilter(b, a, signal) 
plt.figure()
plt.plot(t_vec, signal)

plt.show()
