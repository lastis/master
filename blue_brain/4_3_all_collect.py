"""
Simulation: Gather different data about single neurons.
"""
# pylint: disable=invalid-name
import os
import numpy as np
import LFPy_util
import LFPy_util.plot as lplot
import LFPy_util.colormaps as lcmaps
import LFPy_util.data_extraction as de
import matplotlib.pyplot as plt

dir_input = "4_3_all"
dir_output = "4_3_all_collected"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 3

neuron_names = []
r_vectors = []
widths_mean = []
widths_std = []

# Specify data gather function.
def gather_data(neuron_name, run_param, data):
    """
    Gathers data from the simulations into lists.
    """
    print neuron_name
    neuron_names.append(neuron_name)
    widths_mean.append(data['widths_I_mean'])
    widths_std.append(data['widths_I_std'])
    r_vectors.append(data['bins'])

# Start collecting data and fill the lists.
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()

print "plotting"
lplot.set_rc_param()
fname = 'NBC_neurons'
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(len(neuron_names)+1)
for i in xrange(len(neuron_names)) :
    plt.plot(
            r_vectors[i],
            widths_mean[i],
            color=colors[i],
            marker='o',
            markersize=5,
            )
    ax.fill_between(
            r_vectors[i],
            widths_mean[i] - widths_std[i],
            widths_mean[i] + widths_std[i],
            color=colors[i],
            alpha=0.2
            )

lplot.save_plt(plt, fname, dir_output)
plt.close()
