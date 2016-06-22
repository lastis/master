# pylint: disable=invalid-name, missing-docstring
import handler
import numpy as np
import matplotlib.pyplot as plt
import utils
import warnings
import quantities as pq
import LFPy_util.data_extraction as de
import LFPy_util as lfpyu

handler.download_data()
blocks = handler.get_data()

def spike_matrix_it():
    for block in blocks:
        for rec_ch_gr in block.recordingchannelgroups:
            for unit in rec_ch_gr.units:
                for spiketrain in unit.spiketrains:
                    yield spiketrain.waveforms


sample_freq = blocks[0].recordingchannelgroups[0].units[0].spiketrains[0].sampling_rate
dt = 1.0/sample_freq

for i, spike_matrix in enumerate(spike_matrix_it()):
    spike_mean, spike_std = utils.tetrode_spikes_mean_max(spike_matrix)
    width_III, trace = de.find_wave_width_type_III(spike_mean, dt=dt)
    t_vec = dt*np.arange(spike_matrix.shape[-1])*pq.microsecond*1000
    plt.plot(t_vec, spike_mean)
    plt.plot(t_vec, trace[0])
    ax = plt.gca()
    ax.fill_between(t_vec,
                    spike_mean - spike_std,
                    spike_mean + spike_std,
                    alpha=0.2)
    plt.savefig("spike_{}.png".format(i))
    plt.close()

for i, spike_matrix in enumerate(spike_matrix_it()):
    spike_mean, spike_std = utils.tetrode_spikes_mean_max(spike_matrix)
    width_III, trace = de.find_wave_width_type_III(spike_mean, dt=dt)
    amp = de.find_amplitude_type_II(spike_mean)
    plt.scatter(width_III*1000, amp)
plt.savefig("amp_width_III_max.png")
plt.close()

for i, spike_matrix in enumerate(spike_matrix_it()):
    spike_mean, spike_std = utils.tetrode_spikes_mean_max(spike_matrix)
    width, trace = de.find_wave_width_type_I(spike_mean, dt=dt)
    amp = de.find_amplitude_type_II(spike_mean)
    plt.scatter(width*1000, amp)
plt.savefig("amp_width_I_max.png")
plt.close()

def spikes_mean():
    for block in blocks:
        for rec_ch_gr in block.recordingchannelgroups:
            for unit in rec_ch_gr.units:
                for spiketrain in unit.spiketrains:
                    # Shape becomes (electrodes x time)
                    elec_mean_spikes = np.mean(spiketrain.waveforms, axis=0)
                    yield elec_mean_spikes

n_tetrodes = 0
for block in blocks:
    for rec_ch_gr in block.recordingchannelgroups:
        for unit in rec_ch_gr.units:
            for spiketrain in unit.spiketrains:
                n_tetrodes += 1

color_array = lfpyu.colormaps.get_short_color_array(n_tetrodes, 'viridis')
np.random.shuffle(color_array)

for i, spike_mean in enumerate(spikes_mean()):
    width, trace = de.find_wave_width_type_I(spike_mean, dt)
    width = width*1000
    amp = de.find_amplitude_type_II(spike_mean)
    plt.scatter(width, amp, color=color_array[i])
    plt.savefig('amps_widths_I_{}.png'.format(i))
    plt.close()

for i, spike_mean in enumerate(spikes_mean()):
    width, trace = de.find_wave_width_type_III(spike_mean, dt=dt)
    width = width*1000
    amp = de.find_amplitude_type_II(spike_mean)
    plt.scatter(width, amp, color=color_array[i])
    plt.savefig('amps_widths_III_{}.png'.format(i))
    plt.close()

for i, spike_mean in enumerate(spikes_mean()):
    width, trace = de.find_wave_width_type_I(spike_mean, dt)
    width = width*1000
    amp = de.find_amplitude_type_II(spike_mean)
    plt.scatter(width, amp, color=color_array[i])
plt.savefig('amps_widths_I.png')
plt.close()

for i, spike_mean in enumerate(spikes_mean()):
    width_III, trace = de.find_wave_width_type_III(spike_mean, dt=dt)
    width_III = width_III*1000*dt
    amp = de.find_amplitude_type_II(spike_mean)
    plt.scatter(width_III, amp, color=color_array[i])
plt.savefig('amps_widths_III.png')
plt.close()

# for i, spike_mean in enumerate(spikes_mean()):
#     # if i >= 14: 
#     #     continue
#     width, trace = de.find_wave_width_type_I(spike_mean, dt)
#     width_III, trace = de.find_wave_width_type_III(spike_mean, dt=dt)
#     plt.plot(spike_mean.T)
#     plt.plot(trace.T)
#     plt.show()
#     plt.close()


