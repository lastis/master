# pylint: disable=invalid-name, missing-docstring
import handler
import numpy as np
import matplotlib.pyplot as plt
import LFPy_util.data_extraction as de
import warnings
from scipy.signal import butter, lfilter, filtfilt

handler.download_data()
blocks = handler.get_data()

spiketrain = blocks[0].recordingchannelgroups[2].units[4].spiketrains[0]
signal = spiketrain.waveforms
signal = signal[0].T

plt.figure()
plt.plot(signal)

sample_freq = spiketrain.sampling_rate
dt = 1.0/sample_freq
t_vec = dt*np.arange(signal.shape[0])

freq, amp, phase = de.find_freq_and_fft(dt, signal, axis=0)

plt.figure()
plt.plot(freq, amp)
# plt.plot(amp)

nyq = 0.5 * sample_freq
high = 6700/nyq
low = 300/nyq
b, a = butter(1, [low, high])
signal = lfilter(b, a, signal, axis=0) 
plt.figure()
plt.plot(signal)

plt.show()
