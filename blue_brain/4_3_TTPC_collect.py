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

dir_input = "4_3_TTPC"
dir_output = "4_3_TTPC_collected"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True

neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []

# Specify data gather function.
def gather_data(neuron_name, run_param, data):
    """
    Gathers data from the simulations into lists.
    """
    print neuron_name
    neuron_names.append(neuron_name)
    widths_I_mean.append(data['widths_I_mean'])
    widths_I_std.append(data['widths_I_std'])
    widths_II_mean.append(data['widths_II_mean'])
    widths_II_std.append(data['widths_II_std'])
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
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)

widths_I_mean_combined, widths_I_std_combined = \
    de.combined_mean_std(widths_I_mean, widths_I_std)

widths_II_mean_combined, widths_II_std_combined = \
    de.combined_mean_std(widths_II_mean, widths_II_std)

lplot.set_rc_param()

# {{{ Plot 1
fname = 'TTPC2_width_I_seperate'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(len(neuron_names)+1)
for i in xrange(len(neuron_names)) :
    plt.plot(
            r_vectors[i],
            widths_I_mean[i],
            color=colors[i],
            marker='o',
            markersize=5,
            label=neuron_names[i].replace('_','\_'),
            )
    ax.fill_between(
            r_vectors[i],
            widths_I_mean[i] - widths_I_std[i],
            widths_I_mean[i] + widths_I_std[i],
            color=colors[i],
            alpha=0.2
            )
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,
          labels,
          loc='upper left',
          # bbox_to_anchor=(1, 0.5), 
          )

lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# {{{ Plot 2
fname = 'TTPC2_width_II_seperate'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(len(neuron_names)+1)
for i in xrange(len(neuron_names)) :
    plt.plot(
            r_vectors[i],
            widths_II_mean[i],
            color=colors[i],
            marker='o',
            markersize=5,
            label=neuron_names[i].replace('_','\_'),
            )
    ax.fill_between(
            r_vectors[i],
            widths_II_mean[i] - widths_II_std[i],
            widths_II_mean[i] + widths_II_std[i],
            color=colors[i],
            alpha=0.2
            )
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,
          labels,
          loc='upper left',
          # bbox_to_anchor=(1, 0.5), 
          )

lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# {{{ Plot 3
fname = 'TTPC2_width_I_combined'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(len(neuron_names)+1)
plt.plot(
        r_vectors[0],
        widths_I_mean_combined,
        color=lcmaps.get_color(0),
        marker='o',
        markersize=5,
        )
ax.fill_between(
        r_vectors[i],
        widths_I_mean_combined - widths_I_std_combined,
        widths_I_mean_combined + widths_I_std_combined,
        color=lcmaps.get_color(0),
        alpha=0.2
        )

lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# {{{ Plot 4
fname = 'TTPC2_width_II_combined'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(len(neuron_names)+1)
plt.plot(
        r_vectors[0],
        widths_II_mean_combined,
        color=lcmaps.get_color(0),
        marker='o',
        markersize=5,
        )
ax.fill_between(
        r_vectors[i],
        widths_II_mean_combined - widths_II_std_combined,
        widths_II_mean_combined + widths_II_std_combined,
        color=lcmaps.get_color(0),
        alpha=0.2
        )

lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
