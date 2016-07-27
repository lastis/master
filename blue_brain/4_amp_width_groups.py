"""
Compare width analysis for TTPC and NBC, LBC.
"""
# pylint: disable=invalid-name
import os
import numpy as np
import LFPy_util
import LFPy_util.plot as lplot
import LFPy_util.colormaps as lcmaps
import LFPy_util.data_extraction as de
import matplotlib.pyplot as plt
import sklearn.metrics as metrics

dir_input = "width_sim_all"
dir_output = "4_amp_width_groups"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True

neuron_names = []
widths_I = []
widths_II = []
amps_II = []
dt = None

groups = ['TTPC1', 'LBC_cIR', 'LBC_dSTUT', 'NBC_cNAC', 'NBC', 'PC', \
        "LBC", "TTPC", "UTPC", "TTPC2", "STPC"]

# Specify data gather function.
def gather_data(neuron_name, dir_data, sim):
    """
    Gathers data from the simulations into lists.
    """
    global dt

    if not any(neuron_name for grp in groups if grp in neuron_name):
        return

    print neuron_name

    neuron_names.append(neuron_name)

    sim.load(dir_data)
    sim.process_data()
    data = sim.data

    widths_I.append(data['widths_I'])
    widths_II.append(data['widths_II'])
    amps_II.append(data['amps_I'])
    if dt is None:
        dt = data['dt']
    if data['dt'] != dt:
        raise ValueError("Mismatching simulations.")
    dt = data['dt']

# Collecting data from PC neurons.
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

sort_indices = np.argsort(neuron_names[:])
neuron_names = np.take(neuron_names, sort_indices)
widths_I = np.take(widths_I, sort_indices)
widths_II = np.take(widths_II, sort_indices)
amps_II = np.take(amps_II, sort_indices)

lplot.set_rc_param(True)
lplot.plot_format = ['pdf']

width_bins = np.arange(0, 2.5, dt)
ampli_bins = np.linspace(0,300,80)
bins = [ampli_bins, width_bins]

amp_width_hist = np.zeros([len(neuron_names), len(ampli_bins)-1, len(width_bins)-1])
for i in xrange(len(widths_I)):
    hist, _, _ = np.histogram2d(amps_II[i], widths_I[i], bins)
    hist = hist/float(hist.sum())
    amp_width_hist[i] = hist

for grp in groups:
    hist = np.zeros(amp_width_hist[0].shape)
    for i, name in enumerate(neuron_names):
        if not grp in name: continue
        hist += amp_width_hist[i]
    plt.imshow(hist, 
            interpolation="none", 
            origin='lower',
            extent=[
                width_bins.min(), 
                width_bins.max(), 
                ampli_bins.min(), 
                ampli_bins.max()])
    plt.gca().set_aspect('auto');
    plt.colorbar()
    lplot.save_plt(plt, grp+"_hist_grouped", dir_output)
    plt.close()

# for i, name in enumerate(neuron_names):
#     plt.imshow(amp_width_hist[i], interpolation="nearest", origin='lower')
#     plt.colorbar()
#     lplot.save_plt(plt, name+"_hist", dir_output)
#     plt.close()



