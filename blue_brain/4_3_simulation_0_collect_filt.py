"""
Compare width analysis for TTPC and NBC, LBC.
"""
# pylint: disable=invalid-name
import os
import numpy as np
from itertools import chain
import LFPy_util
import LFPy_util.plot as lplot
import LFPy_util.colormaps as lcmaps
import LFPy_util.data_extraction as de
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse

dir_input = "4_3_simulation_0"
dir_output = "4_3_simulation_0_collected_filt"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRandFilt()
sim_sphere.process_param['filter'] = 'lfilter'
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True
sim_sphere.process_param['freq_low'] = 0.001

# {{{ Define Variables
neuron_check_name = None

neuron_names = []
r_vectors = []
widths_I = []
widths_I_mean = []
widths_I_std = []
widths_II = []
widths_II_mean = []
widths_II_std = []
amps_I = []
amps_I_mean = []
amps_I_std = []
amps_II = []
amps_II_mean = []
amps_II_std = []
# }}} 

# {{{ Reset Variable Function
def reset_variables():
    global neuron_names
    global r_vectors
    global widths_I
    global widths_I_mean
    global widths_I_std
    global widths_II
    global widths_II_mean
    global widths_II_std 
    global amps_I 
    global amps_I_mean
    global amps_I_std
    global amps_II
    global amps_II_mean
    global amps_II_std

    neuron_names = []
    r_vectors = []
    widths_I = []
    widths_I_mean = []
    widths_I_std = []
    widths_II = []
    widths_II_mean = []
    widths_II_std = []
    amps_I = []
    amps_I_mean = []
    amps_I_std = []
    amps_II = []
    amps_II_mean = []
    amps_II_std = []
# }}} 

# {{{ Data Gather Function
# Specify data gather function.
def gather_data(neuron_name, dir_data, sim):
    """
    Gathers data from the simulations into lists.
    """

    if not neuron_check_name in neuron_name:
        return

    print neuron_name
    neuron_names.append(neuron_name)

    sim.load(dir_data)
    sim.process_data()
    data = sim.data

    widths_I.append(data['widths_I'])
    widths_I_mean.append(data['widths_I_mean'])
    widths_I_std.append(data['widths_I_std'])
    widths_II.append(data['widths_II'])
    widths_II_mean.append(data['widths_II_mean'])
    widths_II_std.append(data['widths_II_std'])

    amps_I.append(data['amps_I'])
    amps_I_mean.append(data['amps_I_mean'])
    amps_I_std.append(data['amps_I_std'])
    amps_II.append(data['amps_II'])
    amps_II_mean.append(data['amps_II_mean'])
    amps_II_std.append(data['amps_II_std'])

    r_vectors.append(data['bins'])
# }}} 

# {{{ Format Data Function
def format_data():
    global neuron_names
    global r_vectors
    global widths_I
    global widths_I_mean
    global widths_I_std
    global widths_II
    global widths_II_mean
    global widths_II_std 
    global amps_I 
    global amps_I_mean
    global amps_I_std
    global amps_II
    global amps_II_mean
    global amps_II_std

    # Convert to numpy arrays.
    widths_I_mean = np.array(widths_I_mean)
    widths_I_std = np.array(widths_I_std)
    widths_II_mean = np.array(widths_II_mean)
    widths_II_std = np.array(widths_II_std)
    amps_I_mean = np.array(amps_I_mean)
    amps_I_std = np.array(amps_I_std)
    amps_II_mean = np.array(amps_II_mean)
    amps_II_std = np.array(amps_II_std)

    # Flatten matrices.
    widths_I = np.fromiter(chain.from_iterable(widths_I), np.float)
    widths_II = np.fromiter(chain.from_iterable(widths_II), np.float)
    amps_I = np.fromiter(chain.from_iterable(amps_I), np.float)
    amps_II = np.fromiter(chain.from_iterable(amps_II), np.float)

    # Combine data.
    widths_I_mean, widths_I_std = \
        de.combined_mean_std(widths_I_mean, widths_I_std)
    widths_II_mean, widths_II_std = \
        de.combined_mean_std(widths_II_mean, widths_II_std)
    amps_I_mean, amps_I_std = \
        de.combined_mean_std(amps_I_mean, amps_I_std)
    amps_II_mean, amps_II_std = \
        de.combined_mean_std(amps_II_mean, amps_II_std)

    # Make sure the r_vectors are the same for all simulations.
    for i in xrange(len(neuron_names) - 1):
        if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
            print "Simulations not equal, finishing."
            close()
# }}} 

# {{{ Data PC

reset_variables()

neuron_check_name = 'PC'

# Collecting data from PC neurons.
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

format_data()

# Rename data.
neuron_names_PC = neuron_names

r_vectors_PC = r_vectors

widths_PC_I = widths_I
widths_PC_I_mean = widths_I_mean
widths_PC_I_std = widths_I_std

widths_PC_II = widths_II
widths_PC_II_mean = widths_II_mean
widths_PC_II_std = widths_II_std

amps_PC_I = amps_I
amps_PC_I_mean = amps_I_mean
amps_PC_I_std = amps_I_std

amps_PC_II = amps_II
amps_PC_II_mean = amps_II_mean
amps_PC_II_std = amps_II_std

# }}} 

# {{{ Data LBC

reset_variables()

neuron_check_name = 'LBC'

# Collecting data from LBC neurons.
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

format_data()

# Rename data.
neuron_names_LBC = neuron_names

r_vectors_LBC = r_vectors

widths_LBC_I = widths_I
widths_LBC_I_mean = widths_I_mean
widths_LBC_I_std = widths_I_std

widths_LBC_II = widths_II
widths_LBC_II_mean = widths_II_mean
widths_LBC_II_std = widths_II_std

amps_LBC_I = amps_I
amps_LBC_I_mean = amps_I_mean
amps_LBC_I_std = amps_I_std

amps_LBC_II = amps_II
amps_LBC_II_mean = amps_II_mean
amps_LBC_II_std = amps_II_std

# }}} 

# {{{ Data NBC

reset_variables()

neuron_check_name = 'NBC'

# Collecting data from NBC neurons.
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

format_data()

# Rename data.
neuron_names_NBC = neuron_names

r_vectors_NBC = r_vectors

widths_NBC_I = widths_I
widths_NBC_I_mean = widths_I_mean
widths_NBC_I_std = widths_I_std

widths_NBC_II = widths_II
widths_NBC_II_mean = widths_II_mean
widths_NBC_II_std = widths_II_std

amps_NBC_I = amps_I
amps_NBC_I_mean = amps_I_mean
amps_NBC_I_std = amps_I_std

amps_NBC_II = amps_II
amps_NBC_II_mean = amps_II_mean
amps_NBC_II_std = amps_II_std

# }}} 

# {{{ SNR
SNR_PC_I = widths_PC_I_std/widths_PC_I_mean
SNR_PC_II = widths_PC_II_std/widths_PC_II_mean

SNR_NBC_I = widths_NBC_I_std/widths_NBC_I_mean
SNR_NBC_II = widths_NBC_II_std/widths_NBC_II_mean

SNR_LBC_I = widths_LBC_I_std/widths_LBC_I_mean
SNR_LBC_II = widths_LBC_II_std/widths_LBC_II_mean
# }}} 

lplot.set_rc_param()

# {{{ Plot Scatter
# {{{ Init
fname = 'TTPC2_NBC_LBC_IN_combined_scatter'
print "plotting " + fname
fig = plt.figure(figsize=lplot.size_common)
ax = plt.gca()
colors = lcmaps.get_short_color_array(4)
# }}} 
# {{{ Plot TTPC2 Type I
ax0 = plt.subplot(1,2,1)
lplot.nice_axes(ax0)
ax0.scatter(
        widths_PC_I,
        amps_PC_II,
        color=colors[0],
        alpha=0.1,
        label='TTPC2',
        )
# }}} 
# {{{ Plot NBC Type I
ax0.scatter(
        widths_NBC_I,
        amps_NBC_II,
        color=colors[1],
        alpha=0.1,
        label='NBC',
        )
# }}} 
# {{{ Plot LBC Type I
ax0.scatter(
        widths_LBC_I,
        amps_LBC_II,
        color=colors[2],
        alpha=0.1,
        label='LBC',
        )
# }}} 
# {{{ Horizontal Lines
plt.axhline(
        25,
        )
# }}} 
# {{{ Plot TTPC2 Type II
ax1 = plt.subplot(1,2,2)
lplot.nice_axes(ax1)
ax1.scatter(
        widths_PC_II,
        amps_PC_II,
        color=colors[0],
        alpha=0.1,
        label='TTPC2',
        )
# }}} 
# {{{ Plot NBC Type II
ax1.scatter(
        widths_NBC_II,
        amps_NBC_II,
        color=colors[1],
        alpha=0.1,
        label='NBC',
        )
# }}} 
# {{{ Plot LBC Type II
ax1.scatter(
        widths_LBC_II,
        amps_LBC_II,
        color=colors[2],
        alpha=0.1,
        label='LBC',
        )
# }}} 
# {{{ Horizontal Lines
plt.axhline(
        25,
        )
# }}} 
# {{{ Legend
handles, labels = ax0.get_legend_handles_labels()
plt.figlegend(
        handles, 
        labels, 
        loc='center',
        ncol=3,
        labelspacing=0.,
        bbox_to_anchor=(0.5, 1.00),
        )
# }}} 
# {{{ Labels
ax0.set_ylabel(r"Peak-to-peak Amp. \textbf{[\si{\micro\volt}]}")
ax0.set_xlabel(r"Peak-to-peak Width \textbf{[\si{\milli\second}]}")
ax1.set_xlabel(r"Half Max Width \textbf{[\si{\milli\second}]}")
# }}} 
# {{{ Limits
ax0.set_ylim([0, 200])
ax0.set_xlim([0.0, 2.2])
ax1.set_ylim([0, 200])
ax1.set_xlim([0.0, 2.2])
# }}} 
# {{{ Closing
plt.tight_layout()
lplot.save_plt(plt, fname, dir_output)
# }}} 
# {{{ Limits
ax0.set_ylim([0, 25])
ax0.set_xlim([0.6, 2.2])
ax1.set_ylim([0, 25])
ax1.set_xlim([0.0, 1.0])
# }}} 
# {{{ Closing
fname += '_close'
lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# }}} 
# {{{ Plot Combined
# {{{ Init
fname = 'TTPC2_NBC_LBC_IN_combined'
print "plotting " + fname
fig = plt.figure(figsize=lplot.size_common)
ax = plt.gca()
colors = lcmaps.get_short_color_array(4)
# }}} 
# {{{ Plot TTPC2 Type I
ax0 = plt.subplot(1,2,1)
lplot.nice_axes(ax0)
ax0.plot(widths_PC_I_mean,
        amps_PC_II_mean,
        color=colors[0],
        label='TTPC2',
        marker='o',
        markersize=5, )
for i in xrange(amps_PC_I_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_PC_I_mean[i], amps_PC_II_mean[i]),
            width=2*widths_PC_I_std[i],
            height=2*amps_PC_II_std[i],
            )
    ax0.add_artist(ell)
    ell.set_clip_box(ax0.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[0])
# }}} 
# {{{ Plot NBC Type I
ax0.plot(widths_NBC_I_mean,
        amps_NBC_II_mean,
        color=colors[1],
        label='NBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_NBC_I_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_NBC_I_mean[i], amps_NBC_II_mean[i]),
            width=2*widths_NBC_I_std[i],
            height=2*amps_NBC_II_std[i],
            )
    ax0.add_artist(ell)
    ell.set_clip_box(ax0.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[1])
# }}} 
# {{{ Plot LBC Type I
ax0.plot(widths_LBC_I_mean,
        amps_LBC_II_mean,
        color=colors[2],
        label='LBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_LBC_I_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_LBC_I_mean[i], amps_LBC_II_mean[i]),
            width=2*widths_LBC_I_std[i],
            height=2*amps_LBC_II_std[i],
            )
    ax0.add_artist(ell)
    ell.set_clip_box(ax0.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[2])
# }}} 
# {{{ Horizontal Lines
plt.axhline(
        25,
        )
# }}} 
# {{{ Plot TTPC2 Type II
ax1 = plt.subplot(1,2,2)
lplot.nice_axes(ax1)
ax1.plot(widths_PC_II_mean,
        amps_PC_II_mean,
        color=colors[0],
        label='TTPC2',
        marker='o',
        markersize=5, )
for i in xrange(amps_PC_II_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_PC_II_mean[i], amps_PC_II_mean[i]),
            width=2*widths_PC_II_std[i],
            height=2*amps_PC_II_std[i],
            )
    ax1.add_artist(ell)
    ell.set_clip_box(ax1.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[0])
# }}} 
# {{{ Plot NBC Type II
ax1.plot(widths_NBC_II_mean,
        amps_NBC_II_mean,
        color=colors[1],
        label='NBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_NBC_II_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_NBC_II_mean[i], amps_NBC_II_mean[i]),
            width=2*widths_NBC_II_std[i],
            height=2*amps_NBC_II_std[i],
            )
    ax1.add_artist(ell)
    ell.set_clip_box(ax1.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[1])
# }}} 
# {{{ Plot LBC Type II
ax1.plot(widths_LBC_II_mean,
        amps_LBC_II_mean,
        color=colors[2],
        label='LBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_LBC_II_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_LBC_II_mean[i], amps_LBC_II_mean[i]),
            width=2*widths_LBC_II_std[i],
            height=2*amps_LBC_II_std[i],
            )
    ax1.add_artist(ell)
    ell.set_clip_box(ax1.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[2])
# }}} 
# {{{ Horizontal Lines
plt.axhline(
        25,
        )
# }}} 
# {{{ Legend
handles, labels = ax0.get_legend_handles_labels()
plt.figlegend(
        handles, 
        labels, 
        loc='center',
        ncol=3,
        labelspacing=0.,
        bbox_to_anchor=(0.5, 1.00),
        )
# ax0.legend(handles,
#           labels,
#           loc='upper right',
#           # bbox_to_anchor=(1, 0.5), 
#           )
# handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(handles,
#           labels,
#           loc='upper right',
#           # bbox_to_anchor=(1, 0.5), 
#           )
# }}} 
# {{{ Limits
ax1.set_ylim([0, 200])
ax1.set_xlim([0.0, 1.0])
ax0.set_ylim([0, 200])
ax0.set_xlim([0.6, 2.2])
# }}} 
# {{{ Labels
ax0.set_ylabel(r"Peak-to-peak Amp. \textbf{[\si{\micro\volt}]}")
ax0.set_xlabel(r"Peak-to-peak Width \textbf{[\si{\milli\second}]}")
ax1.set_xlabel(r"Half Max Width \textbf{[\si{\milli\second}]}")
# }}} 
# {{{ Closing
plt.tight_layout()
lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# }}} 
# {{{ Plot Combined Double
# {{{ Init
fname = 'TTPC2_NBC_LBC_IN_combined_double'
print "plotting " + fname
fig = plt.figure(figsize=lplot.size_common)
ax = plt.gca()
colors = lcmaps.get_short_color_array(4)
# }}} 
# {{{ Plot TTPC2 Type I
ax0 = plt.subplot(1,2,1)
lplot.nice_axes(ax0)
ax0.plot(widths_PC_I_mean,
        amps_PC_II_mean,
        color=colors[0],
        label='TTPC2',
        marker='o',
        markersize=5, )
for i in xrange(amps_PC_I_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_PC_I_mean[i], amps_PC_II_mean[i]),
            width=4*widths_PC_I_std[i],
            height=4*amps_PC_II_std[i],
            )
    ax0.add_artist(ell)
    ell.set_clip_box(ax0.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[0])
# }}} 
# {{{ Plot NBC Type I
ax0.plot(widths_NBC_I_mean,
        amps_NBC_II_mean,
        color=colors[1],
        label='NBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_NBC_I_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_NBC_I_mean[i], amps_NBC_II_mean[i]),
            width=4*widths_NBC_I_std[i],
            height=4*amps_NBC_II_std[i],
            )
    ax0.add_artist(ell)
    ell.set_clip_box(ax0.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[1])
# }}} 
# {{{ Plot LBC Type I
ax0.plot(widths_LBC_I_mean,
        amps_LBC_II_mean,
        color=colors[2],
        label='LBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_LBC_I_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_LBC_I_mean[i], amps_LBC_II_mean[i]),
            width=4*widths_LBC_I_std[i],
            height=4*amps_LBC_II_std[i],
            )
    ax0.add_artist(ell)
    ell.set_clip_box(ax0.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[2])
# }}} 
# {{{ Horizontal Lines
plt.axhline(
        25,
        )
# }}} 
# {{{ Plot TTPC2 Type II
ax1 = plt.subplot(1,2,2)
lplot.nice_axes(ax1)
ax1.plot(widths_PC_II_mean,
        amps_PC_II_mean,
        color=colors[0],
        label='TTPC2',
        marker='o',
        markersize=5, )
for i in xrange(amps_PC_II_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_PC_II_mean[i], amps_PC_II_mean[i]),
            width=4*widths_PC_II_std[i],
            height=4*amps_PC_II_std[i],
            )
    ax1.add_artist(ell)
    ell.set_clip_box(ax1.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[0])
# }}} 
# {{{ Plot NBC Type II
ax1.plot(widths_NBC_II_mean,
        amps_NBC_II_mean,
        color=colors[1],
        label='NBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_NBC_II_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_NBC_II_mean[i], amps_NBC_II_mean[i]),
            width=4*widths_NBC_II_std[i],
            height=4*amps_NBC_II_std[i],
            )
    ax1.add_artist(ell)
    ell.set_clip_box(ax1.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[1])
# }}} 
# {{{ Plot LBC Type II
ax1.plot(widths_LBC_II_mean,
        amps_LBC_II_mean,
        color=colors[2],
        label='LBC',
        marker='o',
        markersize=5, )
for i in xrange(amps_LBC_II_mean.shape[0]):
    ell = Ellipse(
            xy=(widths_LBC_II_mean[i], amps_LBC_II_mean[i]),
            width=4*widths_LBC_II_std[i],
            height=4*amps_LBC_II_std[i],
            )
    ax1.add_artist(ell)
    ell.set_clip_box(ax1.bbox)
    ell.set_alpha(0.2)
    ell.set_facecolor(colors[2])
# }}} 
# {{{ Horizontal Lines
plt.axhline(
        25,
        )
# }}} 
# {{{ Legend
handles, labels = ax0.get_legend_handles_labels()
plt.figlegend(
        handles, 
        labels, 
        loc='center',
        ncol=3,
        labelspacing=0.,
        bbox_to_anchor=(0.5, 1.00),
        )
# ax0.legend(handles,
#           labels,
#           loc='upper right',
#           # bbox_to_anchor=(1, 0.5), 
#           )
# handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(handles,
#           labels,
#           loc='upper right',
#           # bbox_to_anchor=(1, 0.5), 
#           )
# }}} 
# {{{ Limits
ax1.set_ylim([0, 200])
ax1.set_xlim([0.0, 1.0])
ax0.set_ylim([0, 200])
ax0.set_xlim([0.6, 2.2])
# }}} 
# {{{ Labels
ax0.set_ylabel(r"Peak-to-peak Amp. \textbf{[\si{\micro\volt}]}")
ax0.set_xlabel(r"Peak-to-peak Width \textbf{[\si{\milli\second}]}")
ax1.set_xlabel(r"Half Max Width \textbf{[\si{\milli\second}]}")
# }}} 
# {{{ Closing
plt.tight_layout()
lplot.save_plt(plt, fname, dir_output)
plt.close()
# }}} 
# }}} 
# # {{{ Plot Widths
# fname = 'TTPC2_NBC_LBC_widths'
# print "plotting " + fname
# plt.figure(figsize=lplot.size_common)
# ax0 = plt.gca()
# colors = lcmaps.get_short_color_array(3)

# ax0 = plt.subplot(2,2,1)
# lplot.nice_axes(ax0)
# # Plot PC.
# plt.plot(
#         r_vectors[0],
#         widths_PC_I_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='TTPC2',
#         )
# ax0.fill_between(
#         r_vectors[0],
#         widths_PC_I_mean - widths_PC_I_std,
#         widths_PC_I_mean + widths_PC_I_std,
#         color=colors[0],
#         alpha=0.2
#         )
# ax1 = plt.subplot(2,2,2, sharey=ax0)
# lplot.nice_axes(ax1)
# # Plot NBC.
# plt.plot(
#         r_vectors[0],
#         widths_NBC_I_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='NBC',
#         )
# ax1.fill_between(
#         r_vectors[0],
#         widths_NBC_I_mean - widths_NBC_I_std,
#         widths_NBC_I_mean + widths_NBC_I_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot LBC.
# plt.plot(
#         r_vectors[0],
#         widths_LBC_I_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='LBC',
#         )
# ax1.fill_between(
#         r_vectors[0],
#         widths_LBC_I_mean - widths_LBC_I_std,
#         widths_LBC_I_mean + widths_LBC_I_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(handles,
#           labels,
#           loc='upper left',
#           # bbox_to_anchor=(1, 0.5), 
#           )

# ax2 = plt.subplot(2,2,3)
# lplot.nice_axes(ax2)
# # Plot PC.
# plt.plot(
#         r_vectors[0],
#         widths_PC_II_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='TTPC2',
#         )
# ax2.fill_between(
#         r_vectors[0],
#         widths_PC_II_mean - widths_PC_II_std,
#         widths_PC_II_mean + widths_PC_II_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot IN.
# plt.plot(
#         r_vectors[0],
#         widths_IN_II_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='All IInter.',
#         )
# ax2.fill_between(
#         r_vectors[0],
#         widths_IN_II_mean - widths_IN_II_std,
#         widths_IN_II_mean + widths_IN_II_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax2.get_legend_handles_labels()
# ax2.legend(handles,
#           labels,
#           loc='upper left',
#           )

# ax3 = plt.subplot(2,2,4, sharey=ax2)
# lplot.nice_axes(ax3)
# # Plot NBC.
# plt.plot(
#         r_vectors[0],
#         widths_NBC_II_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='NBC',
#         )
# ax3.fill_between(
#         r_vectors[0],
#         widths_NBC_II_mean - widths_NBC_II_std,
#         widths_NBC_II_mean + widths_NBC_II_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot LBC.
# plt.plot(
#         r_vectors[0],
#         widths_LBC_II_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='LBC',
#         )
# ax3.fill_between(
#         r_vectors[0],
#         widths_LBC_II_mean - widths_LBC_II_std,
#         widths_LBC_II_mean + widths_LBC_II_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax3.get_legend_handles_labels()
# ax3.legend(handles,
#           labels,
#           loc='upper left',
#           )

# ax0.set_ylim([0.5, 3.1])
# ax2.set_ylim([0.1, 1.3])

# ax0.set_ylabel(r"Peak-to-peak Width \textbf{[\si{\milli\second}]}")
# ax2.set_ylabel(r"Half Max Width \textbf{[\si{\milli\second}]}")
# ax2.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
# ax3.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
# lplot.save_plt(plt, fname, dir_output)
# plt.close()
# # }}} 
# # {{{ Plot Amps
# fname = 'TTPC2_NBC_LBC_IN_amps'
# print "plotting " + fname
# plt.figure(figsize=lplot.size_common)
# ax = plt.gca()
# colors = lcmaps.get_short_color_array(3)

# ax0 = plt.subplot(2,2,1)
# lplot.nice_axes(ax0)
# # Plot PC.
# plt.plot(
#         r_vectors[0],
#         amps_PC_I_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='TTPC2',
#         )
# ax0.fill_between(
#         r_vectors[0],
#         amps_PC_I_mean - amps_PC_I_std,
#         amps_PC_I_mean + amps_PC_I_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot IN.
# plt.plot(
#         r_vectors[0],
#         amps_IN_I_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='All Inter.',
#         )
# ax0.fill_between(
#         r_vectors[0],
#         amps_IN_I_mean - amps_IN_I_std,
#         amps_IN_I_mean + amps_IN_I_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax0.get_legend_handles_labels()
# ax0.legend(handles,
#           labels,
#           loc='upper right',
#           # borderpad=0.1,
#           # labelspacing=0.2,
#           )

# ax1 = plt.subplot(2,2,2, sharey=ax0)
# lplot.nice_axes(ax1)
# # Plot NBC.
# plt.plot(
#         r_vectors[0],
#         amps_NBC_I_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='NBC',
#         )
# ax1.fill_between(
#         r_vectors[0],
#         amps_NBC_I_mean - amps_NBC_I_std,
#         amps_NBC_I_mean + amps_NBC_I_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot LBC.
# plt.plot(
#         r_vectors[0],
#         amps_LBC_I_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='LBC',
#         )
# ax1.fill_between(
#         r_vectors[0],
#         amps_LBC_I_mean - amps_LBC_I_std,
#         amps_LBC_I_mean + amps_LBC_I_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax1.get_legend_handles_labels()
# ax1.legend(handles,
#           labels,
#           loc='upper right',
#           # bbox_to_anchor=(1, 0.5), 
#           )

# ax2 = plt.subplot(2,2,3)
# lplot.nice_axes(ax2)
# # Plot PC.
# plt.plot(
#         r_vectors[0],
#         amps_PC_II_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='TTPC2',
#         )
# ax2.fill_between(
#         r_vectors[0],
#         amps_PC_II_mean - amps_PC_II_std,
#         amps_PC_II_mean + amps_PC_II_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot IN.
# plt.plot(
#         r_vectors[0],
#         amps_IN_II_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='All IInter.',
#         )
# ax2.fill_between(
#         r_vectors[0],
#         amps_IN_II_mean - amps_IN_II_std,
#         amps_IN_II_mean + amps_IN_II_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax2.get_legend_handles_labels()
# ax2.legend(handles,
#           labels,
#           loc='upper right',
#           )

# ax3 = plt.subplot(2,2,4, sharey=ax2)
# lplot.nice_axes(ax3)
# # Plot NBC.
# plt.plot(
#         r_vectors[0],
#         amps_NBC_II_mean,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='NBC',
#         )
# ax3.fill_between(
#         r_vectors[0],
#         amps_NBC_II_mean - amps_NBC_II_std,
#         amps_NBC_II_mean + amps_NBC_II_std,
#         color=colors[0],
#         alpha=0.2
#         )

# # Plot LBC.
# plt.plot(
#         r_vectors[0],
#         amps_LBC_II_mean,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='LBC',
#         )
# ax3.fill_between(
#         r_vectors[0],
#         amps_LBC_II_mean - amps_LBC_II_std,
#         amps_LBC_II_mean + amps_LBC_II_std,
#         color=colors[1],
#         alpha=0.2
#         )

# handles, labels = ax3.get_legend_handles_labels()
# ax3.legend(handles,
#           labels,
#           loc='upper right',
#           )

# ax0.set_ylim([0, 200])
# ax2.set_ylim([0, 200])

# ax0.set_ylabel(r"Base-to-peak Amp. \textbf{[\si{\micro\volt}]}")
# ax2.set_ylabel(r"Peak-to-peak Amp. \textbf{[\si{\micro\volt}]}")
# ax2.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
# ax3.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
# lplot.save_plt(plt, fname, dir_output)
# plt.close()
# # }}} 
# # {{{ Plot Signal to noise
# fname = 'TTPC2_NBC_LBC_IN_snr'
# print "plotting " + fname
# plt.figure(figsize=lplot.size_common)
# colors = lcmaps.get_short_color_array(3)

# ax0 = plt.subplot(2,2,1)
# plt.title('TTPC2')
# lplot.nice_axes(ax0)
# # Plot PC.
# plt.plot(
#         r_vectors[0],
#         SNR_PC_I,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         label='Peak-to-peak Width'
#         )
# plt.plot(
#         r_vectors[0],
#         SNR_PC_II,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         label='Half Max Width'
#         )

# ax1 = plt.subplot(2,2,2, sharey=ax0)
# lplot.nice_axes(ax1)
# plt.title('NBC')
# plt.plot(
#         r_vectors[0],
#         SNR_NBC_I,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         )
# plt.plot(
#         r_vectors[0],
#         SNR_NBC_II,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         )

# ax2 = plt.subplot(2,2,3)
# lplot.nice_axes(ax2)
# plt.title('LBC')
# plt.plot(
#         r_vectors[0],
#         SNR_LBC_I,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         )
# plt.plot(
#         r_vectors[0],
#         SNR_LBC_II,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         )

# ax3 = plt.subplot(2,2,4, sharey=ax2)
# lplot.nice_axes(ax3)
# plt.title('All Inter.')
# plt.plot(
#         r_vectors[0],
#         SNR_IN_I,
#         color=colors[0],
#         marker='o',
#         markersize=5,
#         )
# plt.plot(
#         r_vectors[0],
#         SNR_IN_II,
#         color=colors[1],
#         marker='o',
#         markersize=5,
#         )

# handles, labels = ax0.get_legend_handles_labels()
# plt.figlegend(
#         handles, 
#         labels, 
#         loc='center',
#         ncol=3,
#         labelspacing=0.,
#         bbox_to_anchor=(0.5, 1.00),
#         )

# ax0.set_ylabel(r"$c_v$")
# ax2.set_ylabel(r"$c_v$")
# ax2.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
# ax3.set_xlabel(r"Distance from Soma \textbf{[\si{\micro\metre}]}")
# plt.tight_layout()

# lplot.save_plt(plt, fname, dir_output)
# plt.close()
# # }}} 
