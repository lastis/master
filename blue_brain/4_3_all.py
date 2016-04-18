"""
NBC neurons.
Calculate the width and amp dependency in relation to distance from
soma for NBC neurons with same e-type but different m-type.
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
dir_neurons = os.path.join(dir_current, "4_3_all")

# Download models if they do not exist.
blue_brain.download_all_models(dir_model)

# Names of the neurons that also match the model folders.
os.chdir(dir_model)
neurons = []
neurons += glob('L5_TTPC*_1')
# neurons += glob('L5_NBC*_1')
# neurons += glob('L5_MC*_1')
# neurons += glob('L5_LBC*_1')
# neurons += glob('L5_SBC*_1')

# Compile and load the extra mod file(s). The ISyn electrode.
mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod')
LFPy_util.other.nrnivmodl(mod_dir, suppress=True)


sim = LFPy_util.Simulator()
sim.set_dir_neurons(dir_neurons)
sim.set_neuron_name(neurons)
sim.concurrent_neurons = 6

# Simulation objects.
sim_multi = LFPy_util.sims.MultiSpike()
sim_multi.run_param['pptype'] = 'ISyn'
sim_multi.run_param['threshold'] = 4
sim_multi.run_param['delay'] = 100
sim_multi.run_param['duration'] = 800
sim_multi.run_param['spikes'] = 5
sim_multi.run_param['init_amp'] = 0.10
sim_multi.verbose = True
# sim_multi.only_apply_electrode = True
sim.push(sim_multi, False)

sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.run_param['N'] = 500
sim_sphere.run_param['R'] = 100
sim_sphere.process_param['spike_to_measure'] = 3
sim_sphere.process_param['assert_width'] = True
sim.push(sim_sphere)

sim_morph = LFPy_util.sims.Morphology()
sim.push(sim_morph)

# Define a load model function to send to the simulator.
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

sim.set_cell_load_func(load_func)
sim.assign_seed = 1234

# Simulation
print sim
sim.simulate()
sim.plot()

