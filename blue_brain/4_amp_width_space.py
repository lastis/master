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
dir_output = "4_amp_width_space"

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

# Specify data gather function.
def gather_data(neuron_name, dir_data, sim):
    """
    Gathers data from the simulations into lists.
    """
    global dt

    if not "TTPC1" in neuron_name and not "LBC_cIR" in neuron_name:
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

lplot.set_rc_param(False)
lplot.plot_format = ['png']

amp_width_hist = []
width_bins = np.linspace(0, 2.5, 50)
amp_bins = np.linspace(0,300,50)
bins = [amp_bins, width_bins]
for i in xrange(len(widths_I)):
    hist, _, _ = np.histogram2d(amps_II[i], widths_I[i], bins)
    hist = hist/float(hist.sum())
    amp_width_hist.append(hist)

for i, name in enumerate(neuron_names):
    plt.imshow(amp_width_hist[i], interpolation="nearest", origin='lower')
    plt.colorbar()
    lplot.save_plt(plt, name+"_hist", dir_output)
    plt.close()


