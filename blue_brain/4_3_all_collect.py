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
widths_I_mean = []
widths_I_std = []

# Specify data gather function.
def gather_data(neuron_name, run_param, data):
    """
    Gathers data from the simulations into lists.
    """
    print neuron_name
    neuron_names.append(neuron_name)
    widths_I_mean.append(data['widths_I_mean'])
    widths_I_std.append(data['widths_I_std'])
    r_vectors.append(data['bins'])

# Start collecting data and fill the lists.
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()

widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)

indices_pyramidal = [i for i in xrange(len(neuron_names)) if 'TTPC' in neuron_names[i]]
indices_inter = np.delete(range(len(neuron_names)), indices_pyramidal)

widths_I_mean_pyramidal = widths_I_mean[indices_pyramidal]
widths_I_mean_inter = widths_I_mean[indices_inter]

widths_I_std_pyramidal = widths_I_std[indices_pyramidal]
widths_I_std_inter = widths_I_std[indices_inter]

widths_I_mean_pyramidal, widths_I_std_pyramidal = \
    de.combined_mean_std(widths_I_mean_pyramidal, widths_I_std_pyramidal)

widths_I_mean_inter, widths_I_std_inter = \
    de.combined_mean_std(widths_I_mean_inter, widths_I_std_inter)

print "plotting"
lplot.set_rc_param()
fname = 'pyramidal_inter_neurons'
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)

colors = lcmaps.get_short_color_array(3)

plt.plot(
        r_vectors[0],
        widths_I_mean_pyramidal,
        color=colors[0],
        marker='o',
        markersize=5,
        label='Pyramidal'
        )

ax.fill_between(
        r_vectors[0],
        widths_I_mean_pyramidal - widths_I_std_pyramidal,
        widths_I_mean_pyramidal + widths_I_std_pyramidal,
        color=colors[0],
        alpha=0.2
        )

plt.plot(
        r_vectors[0],
        widths_I_mean_inter,
        color=colors[1],
        marker='o',
        markersize=5,
        label='Inter'
        )

ax.fill_between(
        r_vectors[0],
        widths_I_mean_inter - widths_I_std_inter,
        widths_I_mean_inter + widths_I_std_inter,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,
          labels,
          loc='center left',
          bbox_to_anchor=(1, 0.5), )

lplot.save_plt(plt, fname, dir_output)
plt.close()
