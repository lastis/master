"""
Compare width analysis for TTPC and NBC
"""
# pylint: disable=invalid-name
import os
import numpy as np
import LFPy_util
import LFPy_util.plot as lplot
import LFPy_util.colormaps as lcmaps
import LFPy_util.data_extraction as de
import matplotlib.pyplot as plt

dir_input_NBC = "4_3_NBC"
dir_input_PC = "4_3_TTPC"
dir_input_LBC = "4_3_LBC"
dir_output = "4_3_NBC_TTPC_LBC_collected"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input_NBC = os.path.join(dir_current, dir_input_NBC)
dir_input_PC = os.path.join(dir_current, dir_input_PC)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True

# Specify data gather function.
neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []
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
# {{{ Data PC
# Collecting data from PC neurons.
neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []
LFPy_util.other.collect_data(dir_input_PC, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)

# Rename data.
neuron_names_PC = neuron_names
r_vectors_PC = r_vectors
widths_PC_I_mean = widths_I_mean
widths_PC_I_std = widths_I_std
widths_PC_II_mean = widths_II_mean
widths_PC_II_std = widths_II_std

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()
# }}} 
# {{{ Data NBC
# Collecting data from NBC neurons.
neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []
LFPy_util.other.collect_data(dir_input_NBC, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)

# Rename data.
neuron_names_NBC = neuron_names
r_vectors_NBC = r_vectors
widths_NBC_I_mean = widths_I_mean
widths_NBC_I_std = widths_I_std
widths_NBC_II_mean = widths_II_mean
widths_NBC_II_std = widths_II_std

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()
# }}} 
# {{{ Data LBC
# Collecting data from LBC neurons.
neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []
LFPy_util.other.collect_data(dir_input_LBC, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)

# Rename data.
neuron_names_LBC = neuron_names
r_vectors_LBC = r_vectors
widths_LBC_I_mean = widths_I_mean
widths_LBC_I_std = widths_I_std
widths_LBC_II_mean = widths_II_mean
widths_LBC_II_std = widths_II_std

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()
# }}} 

SNR_PC_I = widths_PC_I_std/widths_PC_I_mean
SNR_PC_II = widths_PC_II_std/widths_PC_II_mean

SNR_NBC_I = widths_NBC_I_std/widths_NBC_I_mean
SNR_NBC_II = widths_NBC_II_std/widths_NBC_II_mean

SNR_LBC_I = widths_LBC_I_std/widths_LBC_I_mean
SNR_LBC_II = widths_LBC_II_std/widths_LBC_II_mean

lplot.set_rc_param()

# {{{ Plot 1
fname = 'TTPC2_NBC_LBC_width_I'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(4)
ax.set_ylabel(r"Width Type I \textbf{[\si{\milli\second}]}")
ax.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")

# Plot PC.
plt.plot(
        r_vectors[0],
        widths_PC_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='TTPC2',
        )
ax.fill_between(
        r_vectors[0],
        widths_PC_I_mean - widths_PC_I_std,
        widths_PC_I_mean + widths_PC_I_std,
        color=colors[0],
        alpha=0.2
        )

# Plot NBC.
plt.plot(
        r_vectors[0],
        widths_NBC_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='NBC',
        )
ax.fill_between(
        r_vectors[0],
        widths_NBC_I_mean - widths_NBC_I_std,
        widths_NBC_I_mean + widths_NBC_I_std,
        color=colors[1],
        alpha=0.2
        )

# Plot LBC.
plt.plot(
        r_vectors[0],
        widths_LBC_I_mean,
        color=colors[2],
        marker='o',
        markersize=5,
        label='LBC',
        )
ax.fill_between(
        r_vectors[0],
        widths_LBC_I_mean - widths_LBC_I_std,
        widths_LBC_I_mean + widths_LBC_I_std,
        color=colors[2],
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
fname = 'TTPC2_NBC_LBC_width_II'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
lplot.nice_axes(ax)
colors = lcmaps.get_short_color_array(4)

ax.set_ylabel(r"Width Type II \textbf{[\si{\milli\second}]}")
ax.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")

# Plot PC.
plt.plot(
        r_vectors[0],
        widths_PC_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='TTPC2',
        )
ax.fill_between(
        r_vectors[0],
        widths_PC_II_mean - widths_PC_II_std,
        widths_PC_II_mean + widths_PC_II_std,
        color=colors[0],
        alpha=0.2
        )

# Plot NBC.
plt.plot(
        r_vectors[0],
        widths_NBC_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='NBC',
        )
ax.fill_between(
        r_vectors[0],
        widths_NBC_II_mean - widths_NBC_II_std,
        widths_NBC_II_mean + widths_NBC_II_std,
        color=colors[1],
        alpha=0.2
        )

# Plot LBC.
plt.plot(
        r_vectors[0],
        widths_LBC_II_mean,
        color=colors[2],
        marker='o',
        markersize=5,
        label='LBC',
        )
ax.fill_between(
        r_vectors[0],
        widths_LBC_II_mean - widths_LBC_II_std,
        widths_LBC_II_mean + widths_LBC_II_std,
        color=colors[2],
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
# {{{ Plot Signal to noise
fname = 'TTPC2_NBC_LBC_snr'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
colors = lcmaps.get_short_color_array(3)

ax0 = plt.subplot(1,3,1)
plt.title('TTPC2')
lplot.nice_axes(ax0)
ax0.set_ylabel(r"SNR")
# Plot PC.
plt.plot(
        r_vectors[0],
        SNR_PC_I,
        color=colors[0],
        marker='o',
        markersize=5,
        label='Type I'
        )
plt.plot(
        r_vectors[0],
        SNR_PC_II,
        color=colors[1],
        marker='o',
        markersize=5,
        label='Type II'
        )
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,
          labels,
          loc='upper left',
          # bbox_to_anchor=(1, 0.5), 
          )

ax1 = plt.subplot(1,3,2, sharey=ax0)
lplot.nice_axes(ax1)
plt.title('NBC')
ax1.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
plt.plot(
        r_vectors[0],
        SNR_NBC_I,
        color=colors[0],
        marker='o',
        markersize=5,
        )
plt.plot(
        r_vectors[0],
        SNR_NBC_II,
        color=colors[1],
        marker='o',
        markersize=5,
        )

ax2 = plt.subplot(1,3,3, sharey=ax0)
lplot.nice_axes(ax2)
plt.title('LBC')
plt.plot(
        r_vectors[0],
        SNR_LBC_I,
        color=colors[0],
        marker='o',
        markersize=5,
        )
plt.plot(
        r_vectors[0],
        SNR_LBC_II,
        color=colors[1],
        marker='o',
        markersize=5,
        )

lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
