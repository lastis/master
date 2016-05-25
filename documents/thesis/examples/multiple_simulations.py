
import os
from glob import glob
import LFPy_util
import blue_brain
import copy

# Gather directory paths.
dir_model = blue_brain.DIR_MODELS
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_output = os.path.join(dir_current, "test")

sim = LFPy_util.Simulator()

# The Simulator will use the neuron name and the 
# load cell function to get the cell object during simulations.
sim.set_neuron_name(neuron_name)
sim.set_cell_load_func(get_cell)
sim.set_output_dir(dir_output)
sim.verbose = True

sim_sweep = LFPy_util.sims.CurrentSweep()
sim_sweep.run_param['pptype'] = 'ISyn'

