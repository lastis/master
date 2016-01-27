# Simulation: Gather different data about single neurons.
import os
import numpy as np
import blue_brain
import LFPy_util
import LFPy_util.plot as lplot

input_dir = "sim_00"
output_dir = "sim_01"

# Select which neuron types to gather data from.
group_labels = [
        'TTPC1',
        'TTPC2',
        'MC',
        'LBC',
        ]

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current,input_dir)
dir_output = os.path.join(dir_current,output_dir)

# Init variables for data collection.
grouped_widths_mean = [[] for _ in xrange(len(group_labels))]
grouped_widths_std = [[] for _ in xrange(len(group_labels))]
grouped_amps_mean = [[] for _ in xrange(len(group_labels))]
grouped_amps_std = [[] for _ in xrange(len(group_labels))]
grouped_distance = [[] for _ in xrange(len(group_labels))]


def gather_data(neuron_name, file_name, run_param, data):
    print neuron_name, file_name
    for i in xrange(len(group_labels)):
        if group_labels[i] not in neuron_name:
            continue
        grouped_widths_mean[i].append(data["widths_II_mean"])
        grouped_widths_std[i].append(data["widths_II_std"])
        grouped_amps_mean[i].append(data["amps_mean"])
        grouped_amps_std[i].append(data["amps_std"])
        grouped_distance[i].append(data["bins"])

# Collect data about all neurons.
sim = LFPy_util.sims.SphereElectrodes()
sim.amp_threshold = 0
LFPy_util.other.collect_data(dir_neurons,sim,gather_data)

# Format the gathered data.
for i, group in enumerate(group_labels):
    if len(grouped_distance[i]) == 0:
        continue
    grouped_widths_mean[i] = np.mean(grouped_widths_mean[i],0)
    grouped_widths_std[i] = np.mean(grouped_widths_std[i],0)
    grouped_amps_mean[i] = np.mean(grouped_amps_mean[i],0)
    grouped_amps_std[i] = np.mean(grouped_amps_std[i],0)
    grouped_distance[i] = np.array(grouped_distance[i][0])
# # New plot.
fname = 'amps_all'
lplot.spike_amps_grouped_new(grouped_amps_mean,grouped_amps_std,
        grouped_distance,group_labels,show=False,
        fname=fname,plot_save_dir=output_dir)

fname = 'widths_all'
lplot.spike_widths_grouped_new(grouped_widths_mean,grouped_widths_std,
        grouped_distance,group_labels,show=False,
        fname=fname,plot_save_dir=output_dir)

fname = 'amps_widths_all'
lplot.spike_widths_and_amps_grouped_new(grouped_widths_mean,grouped_widths_std,
        grouped_amps_mean,grouped_amps_std,
        grouped_distance,group_labels,show=False,
        fname=fname,plot_save_dir=output_dir)

