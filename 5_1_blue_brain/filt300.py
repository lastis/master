"""
Simulation run on several neurons.
"""
# pylint: disable=invalid-name

import os
from glob import glob
import LFPy_util
import blue_brain

# Gather directory paths.
dir_model = blue_brain.DIR_MODELS
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current, "filt300")

# Download models if they do not exist.
blue_brain.download_all_models(dir_model)

# How many neurons from each group to simulate.
nrn_cnt = 1

# Load pyramidal cells in L5.
os.chdir(dir_model)
TTPC1 = glob('L5_*TTPC1*')[:nrn_cnt]
TTPC2 = glob('L5_*TTPC2*')[:nrn_cnt]
MC = glob('L5_*MC*')[:nrn_cnt]
LBC = glob('L5_*LBC*')[:nrn_cnt]

# Gather neurons to be simulated.
# neurons = TTPC1 + TTPC2 + MC + LBC
# neurons = TTPC1 + TTPC2
neurons = TTPC1
# neurons = MC + LBC

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
    cell.tstopms = 300
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    return cell


# Simulation objects.
sim_multi = LFPy_util.sims.MultiSpike()
sim_multi.run_param['pptype'] = 'ISyn'
sim_multi.run_param['threshold'] = 4
sim_multi.run_param['delay'] = 100
sim_multi.run_param['duration'] = 200
sim_multi.run_param['spikes'] = 3
sim_multi.verbose = True
sim_intra = LFPy_util.sims.Intracellular()
sim_morph = LFPy_util.sims.Morphology()
# More simulation objects.
sim_symf = LFPy_util.sims.SymmetryFiltered()
sim_symf.process_param['spike_to_measure'] = 1
sim_symf.process_param['order'] = 2
sim_symf.process_param['filter'] = 'filtfilt'
# sim_symf.plot_param['plot_detailed'] = True
sim_sym = LFPy_util.sims.Symmetry()
sim_sym.process_param['spike_to_measure'] = 1
# sim_sym.plot_param['plot_detailed'] = True

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_func)
sim.set_dir_neurons(dir_neurons)
sim.set_neuron_name(neurons)
# sim.parallel_plot = True

sim.push(sim_multi, False)
sim.push(sim_symf, True)
print sim
sim.simulate()
# sim.plot()
