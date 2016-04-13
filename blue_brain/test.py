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
dir_neurons = os.path.join(dir_current, "test")

# Download models if they do not exist.
blue_brain.download_all_models(dir_model)

# Names of the neurons that also match the model folders.
TTPC1 = []
TTPC1.append('L5_TTPC1_cADpyr232_1')
# TTPC1.append('L5_TTPC1_cADpyr232_2')

# Gather neurons to be simulated.
# neurons = TTPC1 + TTPC2 + MC + LBC
# neurons = TTPC1 + TTPC2
neurons = TTPC1
# neurons = MC
# neurons =  LBC

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
    cell.tstopms = 3000
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
sim_multi.run_param['delay'] = 700
sim_multi.run_param['duration'] = 2000
sim_multi.run_param['spikes'] = 11
sim_multi.run_param['init_amp'] = 0.2944
sim_multi.verbose = True
sim.push(sim_multi, False)

sim_intra = LFPy_util.sims.Intracellular()
sim.push(sim_intra)

sim_morph = LFPy_util.sims.Morphology()
sim.push(sim_morph)

sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 3
sim.push(sim_sphere)

sim_sym = LFPy_util.sims.Symmetry()
sim_sym.process_param['spike_to_measure'] = 4
# sim_sym.plot_param['plot_detailed'] = True
sim.push(sim_sym)

# Simulation
print sim
sim.simulate()
sim.plot()

