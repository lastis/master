"""
Compare width analysis for TTPC and NBC, LBC and "all".
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
dir_input_IN = "4_3_IN"
dir_output = "4_3_TTPC_all_collected"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input_NBC = os.path.join(dir_current, dir_input_NBC)
dir_input_PC = os.path.join(dir_current, dir_input_PC)
dir_input_IN = os.path.join(dir_current, dir_input_IN)
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
amps_I_mean = []
amps_I_std = []
amps_II_mean = []
amps_II_std = []
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
    amps_I_mean.append(data['amps_I_mean'])
    amps_I_std.append(data['amps_I_std'])
    amps_II_mean.append(data['amps_II_mean'])
    amps_II_std.append(data['amps_II_std'])
    r_vectors.append(data['bins'])
# {{{ Data PC
# Collecting data from PC neurons.
neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []
amps_I_mean = []
amps_I_std = []
amps_II_mean = []
amps_II_std = []
LFPy_util.other.collect_data(dir_input_PC, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)
amps_I_mean = np.array(amps_I_mean)
amps_I_std = np.array(amps_I_std)
amps_II_mean = np.array(amps_II_mean)
amps_II_std = np.array(amps_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)
amps_I_mean, amps_I_std = \
    de.combined_mean_std(amps_I_mean, amps_I_std)
amps_II_mean, amps_II_std = \
    de.combined_mean_std(amps_II_mean, amps_II_std)

# Rename data.
neuron_names_PC = neuron_names
r_vectors_PC = r_vectors
widths_PC_I_mean = widths_I_mean
widths_PC_I_std = widths_I_std
widths_PC_II_mean = widths_II_mean
widths_PC_II_std = widths_II_std
amps_PC_I_mean = amps_I_mean
amps_PC_I_std = amps_I_std
amps_PC_II_mean = amps_II_mean
amps_PC_II_std = amps_II_std

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
amps_I_mean = []
amps_I_std = []
amps_II_mean = []
amps_II_std = []
LFPy_util.other.collect_data(dir_input_NBC, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)
amps_I_mean = np.array(amps_I_mean)
amps_I_std = np.array(amps_I_std)
amps_II_mean = np.array(amps_II_mean)
amps_II_std = np.array(amps_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)
amps_I_mean, amps_I_std = \
    de.combined_mean_std(amps_I_mean, amps_I_std)
amps_II_mean, amps_II_std = \
    de.combined_mean_std(amps_II_mean, amps_II_std)

# Rename data.
neuron_names_NBC = neuron_names
r_vectors_NBC = r_vectors
widths_NBC_I_mean = widths_I_mean
widths_NBC_I_std = widths_I_std
widths_NBC_II_mean = widths_II_mean
widths_NBC_II_std = widths_II_std
amps_NBC_I_mean = amps_I_mean
amps_NBC_I_std = amps_I_std
amps_NBC_II_mean = amps_II_mean
amps_NBC_II_std = amps_II_std

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
amps_I_mean = []
amps_I_std = []
amps_II_mean = []
amps_II_std = []
LFPy_util.other.collect_data(dir_input_LBC, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)
amps_I_mean = np.array(amps_I_mean)
amps_I_std = np.array(amps_I_std)
amps_II_mean = np.array(amps_II_mean)
amps_II_std = np.array(amps_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)
amps_I_mean, amps_I_std = \
    de.combined_mean_std(amps_I_mean, amps_I_std)
amps_II_mean, amps_II_std = \
    de.combined_mean_std(amps_II_mean, amps_II_std)

# Rename data.
neuron_names_LBC = neuron_names
r_vectors_LBC = r_vectors
widths_LBC_I_mean = widths_I_mean
widths_LBC_I_std = widths_I_std
widths_LBC_II_mean = widths_II_mean
widths_LBC_II_std = widths_II_std
amps_LBC_I_mean = amps_I_mean
amps_LBC_I_std = amps_I_std
amps_LBC_II_mean = amps_II_mean
amps_LBC_II_std = amps_II_std

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()
# }}} 
# {{{ Data all inter
# Collecting data from LBC neurons.
neuron_names = []
r_vectors = []
widths_I_mean = []
widths_I_std = []
widths_II_mean = []
widths_II_std = []
amps_I_mean = []
amps_I_std = []
amps_II_mean = []
amps_II_std = []
LFPy_util.other.collect_data(dir_input_IN, sim_sphere, gather_data)

# Convert to numpy arrays.
widths_I_mean = np.array(widths_I_mean)
widths_I_std = np.array(widths_I_std)
widths_II_mean = np.array(widths_II_mean)
widths_II_std = np.array(widths_II_std)
amps_I_mean = np.array(amps_I_mean)
amps_I_std = np.array(amps_I_std)
amps_II_mean = np.array(amps_II_mean)
amps_II_std = np.array(amps_II_std)

# Combine data.
widths_I_mean, widths_I_std = \
    de.combined_mean_std(widths_I_mean, widths_I_std)
widths_II_mean, widths_II_std = \
    de.combined_mean_std(widths_II_mean, widths_II_std)
amps_I_mean, amps_I_std = \
    de.combined_mean_std(amps_I_mean, amps_I_std)
amps_II_mean, amps_II_std = \
    de.combined_mean_std(amps_II_mean, amps_II_std)

# Rename data.
neuron_names_IN = neuron_names
r_vectors_IN = r_vectors
widths_IN_I_mean = widths_I_mean
widths_IN_I_std = widths_I_std
widths_IN_II_mean = widths_II_mean
widths_IN_II_std = widths_II_std
amps_IN_I_mean = amps_I_mean
amps_IN_I_std = amps_I_std
amps_IN_II_mean = amps_II_mean
amps_IN_II_std = amps_II_std

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

SNR_IN_I = widths_IN_I_std/widths_IN_I_mean
SNR_IN_II = widths_IN_II_std/widths_IN_II_mean

lplot.set_rc_param()

# {{{ Plot 1
fname = 'TTPC2_NBC_LBC_IN_widths'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
colors = lcmaps.get_short_color_array(3)

ax0 = plt.subplot(2,2,1)
lplot.nice_axes(ax0)
# Plot PC.
plt.plot(
        r_vectors[0],
        widths_PC_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='TTPC2',
        )
ax0.fill_between(
        r_vectors[0],
        widths_PC_I_mean - widths_PC_I_std,
        widths_PC_I_mean + widths_PC_I_std,
        color=colors[0],
        alpha=0.2
        )

# Plot IN.
plt.plot(
        r_vectors[0],
        widths_IN_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='All Inter.',
        )
ax0.fill_between(
        r_vectors[0],
        widths_IN_I_mean - widths_IN_I_std,
        widths_IN_I_mean + widths_IN_I_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax0.get_legend_handles_labels()
ax0.legend(handles,
          labels,
          loc='upper left',
          borderpad=0.1,
          labelspacing=0.2,
          )

ax1 = plt.subplot(2,2,2, sharey=ax0)
lplot.nice_axes(ax1)
# Plot NBC.
plt.plot(
        r_vectors[0],
        widths_NBC_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='NBC',
        )
ax1.fill_between(
        r_vectors[0],
        widths_NBC_I_mean - widths_NBC_I_std,
        widths_NBC_I_mean + widths_NBC_I_std,
        color=colors[0],
        alpha=0.2
        )

# Plot LBC.
plt.plot(
        r_vectors[0],
        widths_LBC_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='LBC',
        )
ax1.fill_between(
        r_vectors[0],
        widths_LBC_I_mean - widths_LBC_I_std,
        widths_LBC_I_mean + widths_LBC_I_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles,
          labels,
          loc='upper left',
          # bbox_to_anchor=(1, 0.5), 
          )

ax2 = plt.subplot(2,2,3)
lplot.nice_axes(ax2)
# Plot PC.
plt.plot(
        r_vectors[0],
        widths_PC_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='TTPC2',
        )
ax2.fill_between(
        r_vectors[0],
        widths_PC_II_mean - widths_PC_II_std,
        widths_PC_II_mean + widths_PC_II_std,
        color=colors[0],
        alpha=0.2
        )

# Plot IN.
plt.plot(
        r_vectors[0],
        widths_IN_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='All IInter.',
        )
ax2.fill_between(
        r_vectors[0],
        widths_IN_II_mean - widths_IN_II_std,
        widths_IN_II_mean + widths_IN_II_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles,
          labels,
          loc='upper left',
          )

ax3 = plt.subplot(2,2,4, sharey=ax2)
lplot.nice_axes(ax3)
# Plot NBC.
plt.plot(
        r_vectors[0],
        widths_NBC_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='NBC',
        )
ax3.fill_between(
        r_vectors[0],
        widths_NBC_II_mean - widths_NBC_II_std,
        widths_NBC_II_mean + widths_NBC_II_std,
        color=colors[0],
        alpha=0.2
        )

# Plot LBC.
plt.plot(
        r_vectors[0],
        widths_LBC_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='LBC',
        )
ax3.fill_between(
        r_vectors[0],
        widths_LBC_II_mean - widths_LBC_II_std,
        widths_LBC_II_mean + widths_LBC_II_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax3.get_legend_handles_labels()
ax3.legend(handles,
          labels,
          loc='upper left',
          )

ax0.set_ylabel(r"Width Type I \textbf{[\si{\milli\second}]}")
ax2.set_ylabel(r"Width Type II \textbf{[\si{\milli\second}]}")
ax2.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
ax3.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# {{{ Plot 2
fname = 'TTPC2_NBC_LBC_IN_amps'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
ax = plt.gca()
colors = lcmaps.get_short_color_array(3)

ax0 = plt.subplot(2,2,1)
lplot.nice_axes(ax0)
# Plot PC.
plt.plot(
        r_vectors[0],
        amps_PC_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='TTPC2',
        )
ax0.fill_between(
        r_vectors[0],
        amps_PC_I_mean - amps_PC_I_std,
        amps_PC_I_mean + amps_PC_I_std,
        color=colors[0],
        alpha=0.2
        )

# Plot IN.
plt.plot(
        r_vectors[0],
        amps_IN_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='All Inter.',
        )
ax0.fill_between(
        r_vectors[0],
        amps_IN_I_mean - amps_IN_I_std,
        amps_IN_I_mean + amps_IN_I_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax0.get_legend_handles_labels()
ax0.legend(handles,
          labels,
          loc='upper left',
          borderpad=0.1,
          labelspacing=0.2,
          )

ax1 = plt.subplot(2,2,2, sharey=ax0)
lplot.nice_axes(ax1)
# Plot NBC.
plt.plot(
        r_vectors[0],
        amps_NBC_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='NBC',
        )
ax1.fill_between(
        r_vectors[0],
        amps_NBC_I_mean - amps_NBC_I_std,
        amps_NBC_I_mean + amps_NBC_I_std,
        color=colors[0],
        alpha=0.2
        )

# Plot LBC.
plt.plot(
        r_vectors[0],
        amps_LBC_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='LBC',
        )
ax1.fill_between(
        r_vectors[0],
        amps_LBC_I_mean - amps_LBC_I_std,
        amps_LBC_I_mean + amps_LBC_I_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax1.get_legend_handles_labels()
ax1.legend(handles,
          labels,
          loc='upper left',
          # bbox_to_anchor=(1, 0.5), 
          )

ax2 = plt.subplot(2,2,3)
lplot.nice_axes(ax2)
# Plot PC.
plt.plot(
        r_vectors[0],
        amps_PC_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='TTPC2',
        )
ax2.fill_between(
        r_vectors[0],
        amps_PC_II_mean - amps_PC_II_std,
        amps_PC_II_mean + amps_PC_II_std,
        color=colors[0],
        alpha=0.2
        )

# Plot IN.
plt.plot(
        r_vectors[0],
        amps_IN_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='All IInter.',
        )
ax2.fill_between(
        r_vectors[0],
        amps_IN_II_mean - amps_IN_II_std,
        amps_IN_II_mean + amps_IN_II_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax2.get_legend_handles_labels()
ax2.legend(handles,
          labels,
          loc='upper left',
          )

ax3 = plt.subplot(2,2,4, sharey=ax2)
lplot.nice_axes(ax3)
# Plot NBC.
plt.plot(
        r_vectors[0],
        amps_NBC_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='NBC',
        )
ax3.fill_between(
        r_vectors[0],
        amps_NBC_II_mean - amps_NBC_II_std,
        amps_NBC_II_mean + amps_NBC_II_std,
        color=colors[0],
        alpha=0.2
        )

# Plot LBC.
plt.plot(
        r_vectors[0],
        amps_LBC_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='LBC',
        )
ax3.fill_between(
        r_vectors[0],
        amps_LBC_II_mean - amps_LBC_II_std,
        amps_LBC_II_mean + amps_LBC_II_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax3.get_legend_handles_labels()
ax3.legend(handles,
          labels,
          loc='upper left',
          )

ax0.set_ylabel(r"Amp Type I \textbf{[\si{\micro\volt}]}")
ax2.set_ylabel(r"Amp Type II \textbf{[\si{\micro\volt}]}")
ax2.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
ax3.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# {{{ Plot Signal to noise
fname = 'TTPC2_NBC_LBC_IN_snr'
print "plotting " + fname
plt.figure(figsize=lplot.size_common)
colors = lcmaps.get_short_color_array(3)

ax0 = plt.subplot(2,2,1)
plt.title('TTPC2')
lplot.nice_axes(ax0)
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
handles, labels = ax0.get_legend_handles_labels()
ax0.legend(handles,
          labels,
          loc='upper left',
          # bbox_to_anchor=(1, 0.5), 
          )

ax1 = plt.subplot(2,2,2, sharey=ax0)
lplot.nice_axes(ax1)
plt.title('NBC')
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

ax2 = plt.subplot(2,2,3)
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

ax3 = plt.subplot(2,2,4, sharey=ax2)
lplot.nice_axes(ax3)
plt.title('All Inter.')
plt.plot(
        r_vectors[0],
        SNR_IN_I,
        color=colors[0],
        marker='o',
        markersize=5,
        )
plt.plot(
        r_vectors[0],
        SNR_IN_II,
        color=colors[1],
        marker='o',
        markersize=5,
        )

ax0.set_ylabel(r"$c_v$")
ax2.set_ylabel(r"$c_v$")
ax2.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
ax3.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
plt.tight_layout()

lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
