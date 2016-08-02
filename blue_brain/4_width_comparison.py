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
import matplotlib as mpl
from itertools import chain
from scipy.stats import linregress

dir_input = "width_sim_all"
dir_output = "4_width_comparison"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True
# sim_sphere.process_param['width_half_thresh'] = 0.2

neuron_names = []
pyr_widths_I = []
pyr_widths_I_mean = []
pyr_widths_I_std = []
pyr_widths_II = []
pyr_widths_II_mean = []
pyr_widths_II_std = []
pyr_amps_I = []
pyr_amps_I_mean = []
pyr_amps_I_std = []
pyr_amps_II = []
pyr_amps_II_mean = []
pyr_amps_II_std = []
int_widths_I = []
int_widths_I_mean = []
int_widths_I_std = []
int_widths_II = []
int_widths_II_mean = []
int_widths_II_std = []
int_amps_I = []
int_amps_I_mean = []
int_amps_I_std = []
int_amps_II = []
int_amps_II_mean = []
int_amps_II_std = []
r_vectors = []
dt = None

pyram = 'pyramidal'
inter = 'inter'
cnt_pyr = 0
cnt_int = 0
# Specify data gather function.
def gather_data(neuron_name, dir_data, sim):
    """
    Gathers data from the simulations into lists.
    """
    # global cnt_int
    # global cnt_pyr
    # if 'PC' in neuron_name:
    #     cnt_pyr += 1
    #     if cnt_pyr > 20:
    #         return
    # else:
    #     cnt_int += 1
    #     if cnt_int > 20:
    #         return
    global dt

    print neuron_name

    neuron_names.append(neuron_name)

    sim.load(dir_data)
    sim.process_data()
    data = sim.data

    r_vectors.append(data['bins'])
    if 'PC' in neuron_name:
        pyr_widths_I.append(data['widths_I'])
        pyr_widths_I_mean.append(data['widths_I_mean'])
        pyr_widths_I_std.append(data['widths_I_std'])
        pyr_widths_II.append(data['widths_II'])
        pyr_widths_II_mean.append(data['widths_II_mean'])
        pyr_widths_II_std.append(data['widths_II_std'])

        pyr_amps_I.append(data['amps_I'])
        pyr_amps_I_mean.append(data['amps_I_mean'])
        pyr_amps_I_std.append(data['amps_I_std'])
        pyr_amps_II.append(data['amps_II'])
        pyr_amps_II_mean.append(data['amps_II_mean'])
        pyr_amps_II_std.append(data['amps_II_std'])
    else:
        int_widths_I.append(data['widths_I'])
        int_widths_I_mean.append(data['widths_I_mean'])
        int_widths_I_std.append(data['widths_I_std'])
        int_widths_II.append(data['widths_II'])
        int_widths_II_mean.append(data['widths_II_mean'])
        int_widths_II_std.append(data['widths_II_std'])

        int_amps_I.append(data['amps_I'])
        int_amps_I_mean.append(data['amps_I_mean'])
        int_amps_I_std.append(data['amps_I_std'])
        int_amps_II.append(data['amps_II'])
        int_amps_II_mean.append(data['amps_II_mean'])
        int_amps_II_std.append(data['amps_II_std'])

    if dt is None:
        dt = data['dt']
    if data['dt'] != dt:
        raise ValueError("Mismatching simulations.")
    dt = data['dt']

# Collect data
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

# Make sure the r_vectors are the same for all simulations.
for i in xrange(len(neuron_names) - 1):
    if not np.array_equal(r_vectors[i], r_vectors[i+1]) :
        print "Simulations not equal, finishing."
        close()
r = r_vectors[0]

# width_bins = np.arange(0, 2.5, dt)
# ampli_bins = np.linspace(0,300, len(width_bins))

# {{{ Format data. 
# Flatten matrices. Each list entry are the data from all electrodes 
# each neuron. Flatten so all electrodes from the neurons are together.
pyr_widths_I = np.fromiter(chain.from_iterable(pyr_widths_I), np.float)
pyr_widths_II = np.fromiter(chain.from_iterable(pyr_widths_II), np.float)
pyr_amps_I = np.fromiter(chain.from_iterable(pyr_amps_I), np.float)
pyr_amps_II = np.fromiter(chain.from_iterable(pyr_amps_II), np.float)

int_widths_I = np.fromiter(chain.from_iterable(int_widths_I), np.float)
int_widths_II = np.fromiter(chain.from_iterable(int_widths_II), np.float)
int_amps_I = np.fromiter(chain.from_iterable(int_amps_I), np.float)
int_amps_II = np.fromiter(chain.from_iterable(int_amps_II), np.float)

# Combine std and mean data from nesten lists into a single array.
pyr_widths_I_mean, pyr_widths_I_std = \
    de.combined_mean_std(pyr_widths_I_mean, pyr_widths_I_std)
pyr_widths_II_mean, pyr_widths_II_std = \
    de.combined_mean_std(pyr_widths_II_mean, pyr_widths_II_std)
pyr_amps_I_mean, pyr_amps_I_std = \
    de.combined_mean_std(pyr_amps_I_mean, pyr_amps_I_std)
pyr_amps_II_mean, pyr_amps_II_std = \
    de.combined_mean_std(pyr_amps_II_mean, pyr_amps_II_std)

int_widths_I_mean, int_widths_I_std = \
    de.combined_mean_std(int_widths_I_mean, int_widths_I_std)
int_widths_II_mean, int_widths_II_std = \
    de.combined_mean_std(int_widths_II_mean, int_widths_II_std)
int_amps_I_mean, int_amps_I_std = \
    de.combined_mean_std(int_amps_I_mean, int_amps_I_std)
int_amps_II_mean, int_amps_II_std = \
    de.combined_mean_std(int_amps_II_mean, int_amps_II_std)

start_cutoff = 3
r = r[start_cutoff:]
pyr_widths_I       =  pyr_widths_I[start_cutoff:]
pyr_widths_I_mean  =  pyr_widths_I_mean[start_cutoff:]
pyr_widths_I_std   =  pyr_widths_I_std[start_cutoff:]
pyr_widths_II      =  pyr_widths_II[start_cutoff:] 
pyr_widths_II_mean =  pyr_widths_II_mean[start_cutoff:]
pyr_widths_II_std  =  pyr_widths_II_std[start_cutoff:]
pyr_amps_I         =  pyr_amps_I[start_cutoff:]
pyr_amps_I_mean    =  pyr_amps_I_mean[start_cutoff:]
pyr_amps_I_std     =  pyr_amps_I_std[start_cutoff:]
pyr_amps_II        =  pyr_amps_II[start_cutoff:]
pyr_amps_II_mean   =  pyr_amps_II_mean[start_cutoff:]
pyr_amps_II_std    =  pyr_amps_II_std[start_cutoff:]
int_widths_I       =  int_widths_I[start_cutoff:]
int_widths_I_mean  =  int_widths_I_mean[start_cutoff:] 
int_widths_I_std   =  int_widths_I_std[start_cutoff:]
int_widths_II      =  int_widths_II[start_cutoff:]
int_widths_II_mean =  int_widths_II_mean[start_cutoff:] 
int_widths_II_std  =  int_widths_II_std[start_cutoff:] 
int_amps_I         =  int_amps_I[start_cutoff:]
int_amps_I_mean    =  int_amps_I_mean[start_cutoff:]
int_amps_I_std     =  int_amps_I_std[start_cutoff:]
int_amps_II        =  int_amps_II[start_cutoff:]
int_amps_II_mean   =  int_amps_II_mean[start_cutoff:]
int_amps_II_std    =  int_amps_II_std[start_cutoff:]
# }}} 

lplot.set_rc_param(True)
lplot.plot_format = ['pdf', 'png']

# {{{ Plot interneuron and pyramidal amp. coefficient of var.
fig, ax = plt.subplots(1,2, 
        sharex=True,
        sharey=True,
        figsize=lplot.size_common)

lplot.nice_axes(ax[0])
lplot.nice_axes(ax[1])
ax[0].set_title('Base-to-Peak $c_v$')
ax[1].set_title('Peak-to-Peak $c_v$')

colors = lcmaps.get_short_color_array(3)

ax[0].plot(
        r,
        pyr_amps_I_std/pyr_amps_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label=pyram,
        )
ax[0].plot(
        r,
        int_amps_I_std/int_amps_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label=inter,
        )

ax[1].plot(
        r,
        pyr_amps_II_std/pyr_amps_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label=pyram,
        )
ax[1].plot(
        r,
        int_amps_II_std/int_amps_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label=inter,
        )

handles, labels = ax[0].get_legend_handles_labels()
ax[1].legend(handles,
          labels,
          loc='lower right',
          # bbox_to_anchor=(1, 0.5), 
          )
lplot.save_plt(plt, "int_pyr_amps_snr", dir_output)
plt.close()
# }}} 

# {{{ Plot interneuron and pyramidal coefficient of var.
fig, ax = plt.subplots(1,2, 
        sharex=True,
        sharey=True,
        figsize=lplot.size_common)

lplot.nice_axes(ax[0])
lplot.nice_axes(ax[1])
ax[0].set_title('Peak-to-Peak $c_v$')
ax[1].set_title('Half Amplitude $c_v$')

colors = lcmaps.get_short_color_array(3)

ax[0].plot(
        r,
        pyr_widths_I_std/pyr_widths_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label=pyram,
        )
ax[0].plot(
        r,
        int_widths_I_std/int_widths_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label=inter,
        )

ax[1].plot(
        r,
        pyr_widths_II_std/pyr_widths_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label=pyram,
        )
ax[1].plot(
        r,
        int_widths_II_std/int_widths_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label=inter,
        )

handles, labels = ax[0].get_legend_handles_labels()
ax[1].legend(handles,
          labels,
          loc='lower right',
          # bbox_to_anchor=(1, 0.5), 
          )
lplot.save_plt(plt, "int_pyr_widths_snr", dir_output)
plt.close()
# }}} 

# {{{ Plot interneuron and pyramidal spike widths
fig, ax = plt.subplots(1,2, 
        sharex=True,
        sharey=True,
        figsize=lplot.size_common)

lplot.nice_axes(ax[0])
lplot.nice_axes(ax[1])
ax[0].set_title('Peak-to-Peak Width')
ax[1].set_title('Half Amplitude Width')

colors = lcmaps.get_short_color_array(3)

ax[0].plot(
        r,
        pyr_widths_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label=pyram,
        )
ax[0].fill_between(
        r,
        pyr_widths_I_mean - pyr_widths_I_std,
        pyr_widths_I_mean + pyr_widths_I_std,
        color=colors[0],
        alpha=0.2
        )
ax[0].plot(
        r,
        int_widths_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label=inter,
        )
ax[0].fill_between(
        r,
        int_widths_I_mean - int_widths_I_std,
        int_widths_I_mean + int_widths_I_std,
        color=colors[1],
        alpha=0.2
        )
ax[1].plot(
        r,
        pyr_widths_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='PC',
        )
ax[1].fill_between(
        r,
        pyr_widths_II_mean - pyr_widths_II_std,
        pyr_widths_II_mean + pyr_widths_II_std,
        color=colors[0],
        alpha=0.2
        )
ax[1].plot(
        r,
        int_widths_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='PC',
        )

ax[1].fill_between(
        r,
        int_widths_II_mean - int_widths_II_std,
        int_widths_II_mean + int_widths_II_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax[0].get_legend_handles_labels()
ax[1].legend(handles,
          labels,
          loc='upper right',
          # bbox_to_anchor=(1, 0.5), 
          )
lplot.save_plt(plt, "int_pyr_widths_dist", dir_output)
plt.close()
# }}} 

# {{{ Plot interneuron and pyramidal spike amplitudes
fig, ax = plt.subplots(1,2, 
        sharex=True,
        sharey=True,
        figsize=lplot.size_common)

lplot.nice_axes(ax[0])
lplot.nice_axes(ax[1])
ax[0].set_title('Base-to-Peak Amplitude')
ax[1].set_title('Peak-to-Peak Amplitude')

colors = lcmaps.get_short_color_array(3)

ax[0].plot(
        r,
        pyr_amps_I_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label=pyram,
        )
ax[0].fill_between(
        r,
        pyr_amps_I_mean - pyr_amps_I_std,
        pyr_amps_I_mean + pyr_amps_I_std,
        color=colors[0],
        alpha=0.2
        )
ax[0].plot(
        r,
        int_amps_I_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label=inter,
        )
ax[0].fill_between(
        r,
        int_amps_I_mean - int_amps_I_std,
        int_amps_I_mean + int_amps_I_std,
        color=colors[1],
        alpha=0.2
        )
ax[1].plot(
        r,
        pyr_amps_II_mean,
        color=colors[0],
        marker='o',
        markersize=5,
        label='PC',
        )
ax[1].fill_between(
        r,
        pyr_amps_II_mean - pyr_amps_II_std,
        pyr_amps_II_mean + pyr_amps_II_std,
        color=colors[0],
        alpha=0.2
        )
ax[1].plot(
        r,
        int_amps_II_mean,
        color=colors[1],
        marker='o',
        markersize=5,
        label='PC',
        )

ax[1].fill_between(
        r,
        int_amps_II_mean - int_amps_II_std,
        int_amps_II_mean + int_amps_II_std,
        color=colors[1],
        alpha=0.2
        )

handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles,
          labels,
          loc='upper right',
          # bbox_to_anchor=(1, 0.5), 
          )
lplot.save_plt(plt, "int_pyr_amps_dist", dir_output)
plt.close()
# }}} 

# {{{ Save some data to text file.
info = open(dir_output+'/data.txt', 'w')
slope, intercept, r_value, p_value, std_err = linregress(r, pyr_widths_I_mean)
info.write('pyr width I slope = {}\n'.format(slope))
slope, intercept, r_value, p_value, std_err = linregress(r, int_widths_I_mean)
info.write('int width I slope = {}\n'.format(slope))
slope, intercept, r_value, p_value, std_err = linregress(r, pyr_widths_II_mean)
info.write('pyr width II slope = {}\n'.format(slope))
slope, intercept, r_value, p_value, std_err = linregress(r, int_widths_II_mean)
info.write('int width II slope = {}\n'.format(slope))
info.close()
# }}} 
