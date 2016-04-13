"""
Simulation run on several neurons.
"""
# pylint: disable=invalid-name

import os
from glob import glob
import LFPy_util
import blue_brain
import copy

# Gather directory paths.
dir_model = blue_brain.DIR_MODELS
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current, "4_2_spike_width")

# Download models if they do not exist.
blue_brain.download_all_models(dir_model)

# Names of the neurons that also match the model folders.
neurons = []
neurons.append('L5_TTPC1_cADpyr232_1')

# Compile and load the extra mod file(s). The ISyn electrode.
mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod')
LFPy_util.other.nrnivmodl(mod_dir, suppress=True)

def load_func(neuron):
    """
    Function that loads a cell using the name of the neuron.
    """
    nrn_full = os.path.join(dir_model, neuron)
    cell_list = blue_brain.load_model(nrn_full, suppress=True)
    cell = cell_list[0]
    cell.tstartms = 0
    cell.tstopms = 1000
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    return cell

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_func)
sim.set_dir_neurons(dir_neurons)
sim.set_neuron_name(neurons)

# Simulation objects.
sim_multi = LFPy_util.sims.MultiSpike()
sim_multi.run_param['pptype'] = 'ISyn'
sim_multi.run_param['threshold'] = 4
sim_multi.run_param['delay'] = 100
sim_multi.run_param['duration'] = 800
sim_multi.run_param['spikes'] = 5
sim_multi.run_param['init_amp'] = 0.30
sim_multi.verbose = True
# sim_multi.only_apply_electrode = True
sim.push(sim_multi, False)

sim_width = LFPy_util.sims.SpikeWidthDef()
sim_width.run_param['seed'] = 1
sim_width.process_param['spike_to_measure'] = 3
sim.push(sim_width)

# Simulation
print sim
sim.simulate()
sim.plot()

