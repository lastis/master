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

dir_input = "4_3_width_similarity"
dir_output = "4_3_width_similarity_collected"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True
# sim_sphere.process_param['width_half_thresh'] = 0.2

# {{{ Define Variables
neuron_check_name = None

neuron_names = []
r_vectors = []
elec_r = []
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
    global elec_r
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
    elec_r = []
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
    elec_r.append(data['elec_r'])
# }}} 

# {{{ Format Data Function
def format_data():
    global neuron_names
    global r_vectors
    global elec_r
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

    # Flatten matrices. Each list entry are the data from all electrodes 
    # each neuron. Flatten so all electrodes from the neurons are together.
    widths_I = np.fromiter(chain.from_iterable(widths_I), np.float)
    widths_II = np.fromiter(chain.from_iterable(widths_II), np.float)
    amps_I = np.fromiter(chain.from_iterable(amps_I), np.float)
    amps_II = np.fromiter(chain.from_iterable(amps_II), np.float)
    elec_r = np.fromiter(chain.from_iterable(elec_r), np.float)

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
elec_r_PC = elec_r

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
elec_r_LBC = elec_r

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
elec_r_NBC = elec_r

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

lplot.set_rc_param(False)

