"""
Simulation: Gather different data about single neurons.
"""
# pylint: disable=invalid-name
import os
import numpy as np
import LFPy_util
import LFPy_util.plot as lplot
import LFPy_util.data_extraction as de

input_dir = "filt"
# output_dir = "filt_collect_singles"
output_dir = "collect_singles"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current, input_dir)
dir_output = os.path.join(dir_current, output_dir)

# Init variables for data collection.
group_labels = []
grouped_widths_I_mean = []
grouped_widths_I_std = []
grouped_amps_I_mean = []
grouped_amps_I_std = []
grouped_widths_II_mean = []
grouped_widths_II_std = []
grouped_amps_II_mean = []
grouped_amps_II_std = []
grouped_distance = []


def gather_data(neuron_name, file_name, run_param, data):
    """
    Gathers data from the simulations into lists.
    """
    # pylint: disable=unused-argument

    print neuron_name, file_name
    neuron_name = neuron_name.replace("_", "\_")
    group_labels.append(neuron_name)
    grouped_widths_I_mean.append(data["widths_I_mean"])
    grouped_widths_I_std.append(data["widths_I_std"])
    grouped_amps_I_mean.append(data["amps_I_mean"]*1000)
    grouped_amps_I_std.append(data["amps_I_std"]*1000)
    grouped_widths_II_mean.append(data["widths_II_mean"])
    grouped_widths_II_std.append(data["widths_II_std"])
    grouped_amps_II_mean.append(data["amps_II_mean"]*1000)
    grouped_amps_II_std.append(data["amps_II_std"]*1000)
    grouped_distance.append(data["bins"])

# Collect data about all neurons.
# sim = LFPy_util.sims.SphereRandFilt()
sim = LFPy_util.sims.SphereRand()
LFPy_util.other.collect_data(dir_neurons, sim, gather_data)

# # New plot.
fname = 'amps_I_all'
lplot.spike_amps_grouped_new(grouped_amps_I_mean,
                             grouped_amps_I_std,
                             grouped_distance,
                             group_labels,
                             show=False,
                             fname=fname,
                             plot_save_dir=output_dir)

fname = 'widths_I_all'
lplot.spike_widths_grouped_new(grouped_widths_I_mean,
                               grouped_widths_I_std,
                               grouped_distance,
                               group_labels,
                               show=False,
                               fname=fname,
                               plot_save_dir=output_dir)

fname = 'amps_widths_I_all'
lplot.spike_widths_and_amps_grouped_new(grouped_widths_I_mean,
                                        grouped_widths_I_std,
                                        grouped_amps_II_mean,
                                        grouped_amps_II_std,
                                        grouped_distance,
                                        group_labels,
                                        show=False,
                                        fname=fname,
                                        plot_save_dir=output_dir)

fname = 'amps_II_all'
lplot.spike_amps_grouped_new(grouped_amps_II_mean,
                             grouped_amps_II_std,
                             grouped_distance,
                             group_labels,
                             show=False,
                             fname=fname,
                             plot_save_dir=output_dir)

fname = 'widths_II_all'
lplot.spike_widths_grouped_new(grouped_widths_II_mean,
                               grouped_widths_II_std,
                               grouped_distance,
                               group_labels,
                               show=False,
                               fname=fname,
                               plot_save_dir=output_dir)

fname = 'amps_widths_II_all'
lplot.spike_widths_and_amps_grouped_new(grouped_widths_II_mean,
                                        grouped_widths_II_std,
                                        grouped_amps_II_mean,
                                        grouped_amps_II_std,
                                        grouped_distance,
                                        group_labels,
                                        show=False,
                                        fname=fname,
                                        plot_save_dir=output_dir)
