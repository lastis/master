# Simulation: Gather different data about single neurons.
import blue_brain
import LFPy_util
import os
import sys
from pprint import pprint
from glob import glob
from multiprocessing import Process

input_dir = "sim_00/neurons"
output_dir = "sim_02/"

# Select which neuron types to gather data from.
group_labels = [
        'TTPC1',
        'TTPC2',
        'UTPC',
        'STPC',
        'MC',
        'BTC',
        'DBC',
        'BP',
        'NGC',
        'LBC',
        'NBC',
        'SBC',
        'ChC',
        ]

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current,input_dir)
dir_output = os.path.join(dir_current,output_dir)

# Init variables for data collection.
grouped_widths = [[] for _ in xrange(len(group_labels))]
grouped_amps = [[] for _ in xrange(len(group_labels))]
grouped_elec_pos = [[] for _ in xrange(len(group_labels))]


def gather_data(neuron_name, file_name, run_param, data):
    for i in xrange(len(group_labels)):
        if group_labels[i] not in neuron_name:
            continue
        grouped_widths[i].append(data["widths"])
        grouped_amps[i].append(data["amps"])
        grouped_elec_pos[i].append(data["electrode_pos_r"])

# Collect data about all neurons.
sim = LFPy_util.sims.DiscElectrodes()
LFPy_util.other.collect_data(dir_neurons,sim,gather_data)

for i, group in enumerate(group_labels):
    if len(grouped_widths[i]) == 0:
        continue
    LFPy_util.plot.spike_widths_grouped(
            [grouped_widths[i]],
            [grouped_elec_pos[i]],
            show=False,
            fname=group+'_width_plot',
            group_labels=[group],
            mode='std',
            scale='linear',
            plot_save_dir=dir_output,
            )
    LFPy_util.plot.spike_amps_grouped(
            [grouped_amps[i]],
            [grouped_elec_pos[i]],
            show=False,
            fname=group+'_amp_plot',
            group_labels=[group],
            mode='std',
            scale='linear',
            plot_save_dir=dir_output
            )
    LFPy_util.plot.spike_widths_and_amp_grouped(
            [grouped_widths[i]],
            [grouped_amps[i]],
            [grouped_elec_pos[i]],
            show=False,
            fname=group+'_amp_and_width_plot',
            group_labels=[group],
            plot_save_dir=dir_output
            )





















