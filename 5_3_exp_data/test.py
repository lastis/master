# pylint: disable=invalid-name, missing-docstring
import handler
import numpy as np
import matplotlib.pyplot as plt
import LFPy_util.data_extraction as de
import warnings
import quantities as pq
from scipy.signal import butter, lfilter, filtfilt

handler.download_data()
blocks = handler.get_data()

spiketrain = blocks[0].recordingchannelgroups[2].units[4].spiketrains[0]

signal = spiketrain.waveforms
spike_mean = de.tetrode_spikes_mean(signal)

sample_freq = spiketrain.sampling_rate
dt = 1.0/sample_freq
t_vec = dt*np.arange(signal.shape[-1])*pq.microsecond/pq.micro

plt.figure()
plt.plot(t_vec, spike_mean)
plt.title("original")
plt.savefig("original.png")

# freq, amp, phase = de.find_freq_and_fft(dt, spike_mean)
# freq = freq / 1000

# plt.figure()
# plt.plot(freq, amp)

nyq = 0.5 * sample_freq
high = 6700/nyq
low = 300/nyq
b, a = butter(1, [low, high])

filtered_spike = filtfilt(b, a, spike_mean) 
plt.figure()
plt.plot(t_vec, filtered_spike)
plt.title("filtfilt")
plt.savefig("filtfilt.png")

filtered_spike = lfilter(b, a, spike_mean) 
plt.figure()
plt.plot(t_vec, filtered_spike)
plt.title("lfilter")
plt.savefig("lfilter.png")

