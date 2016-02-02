"""
Simulation: Get the same results as torbjorn.
"""
# pylint: disable=invalid-name

import os
from glob import glob
import LFPy_util
import LFPy
import blue_brain

# Gather directory paths.
dir_model = blue_brain.DIR_MODELS
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current, "sim_02")

# Download models if they do not exist.
blue_brain.download_all_models(dir_model)


# Load pyramidal cells in L5.
os.chdir(dir_model)
TTPC2 = glob('L5_*TTPC2*232_2')

# Gather neurons to be simulated.
neurons = TTPC2

# Compile and load the extra mod file(s). The ISyn electrode.
mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod/')
LFPy_util.other.nrnivmodl(mod_dir)


def load_func(neuron):
    """
    Function that loads a cell using the name of the neuron.
    """
    nrn_full = os.path.join(dir_model, neuron)
    cell_list = blue_brain.load_model(nrn_full)
    cell = cell_list[0]
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    return cell

def insert_sym(cell):
    """
    Function to be run by simulator.
    """
    cell.tstopms = 1200
    cell.tstartms = 0
    # for sec in cell.allseclist:
    #     if 'soma' in sec.name():
    #         syn = neuron.h.ISyn(0.5,sec=sec)
    # syn.dur = 1000
    # syn.delay = 200
    # ...
    soma_clamp_params = {
        'idx': cell.somaidx,
        'record_current': True,
        'amp': 0.23,  #  [nA]
        'dur': 1000,  # [ms]
        'delay': 200,  # [ms]
        'pptype': 'ISyn',
    }
    stim = LFPy.StimIntElectrode(cell, **soma_clamp_params)

    

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_func)
sim.set_dir_neurons(dir_neurons)
sim.set_neuron_name(neurons)
sim.simulate = True
sim.plot = True

# Simulation objects.
sim_single_spike = LFPy_util.sims.SingleSpike()
sim_single_spike.run_param['pptype'] = 'ISyn'
sim_intra = LFPy_util.sims.Intracellular()

sim.push(insert_sym, False)
sim.push(sim_intra, False)

print sim
sim.run()
