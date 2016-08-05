"""
LBC neurons.
Calculate the width and amp dependency in relation to distance from
soma for LBC neurons with different e-type but same m-type.
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
dir_output = os.path.join(dir_current, "4_sim_comparison_pre")

def get_cell(neuron_name):
    """
    Function that loads a cell using the name of the neuron.
    """
    nrn_full = os.path.join(dir_model, neuron_name)
    cell_list = blue_brain.load_model(nrn_full, suppress=True)
    cell = cell_list[0]
    cell.tstartms = -100
    cell.tstopms = 1000
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    return cell

def get_simulator(neuron_name):
    """
    Creates a simulator object from the neuron name.
    """
    sim = LFPy_util.Simulator()

    # The Simulator will use the neuron name and the 
    # load cell function to get the cell object during simulations.
    sim.set_neuron_name(neuron_name)
    sim.set_cell_load_func(get_cell)
    sim.set_output_dir(dir_output)
    sim.verbose = True

    sim_1 = LFPy_util.sims.MultiSpike()
    sim_1.set_name('freq_1')
    sim_1.run_param['pptype'] = 'ISyn'
    sim_1.run_param['threshold'] = 4
    sim_1.run_param['delay'] = 100
    sim_1.run_param['duration'] = 1000
    sim_1.run_param['spikes'] = 1
    sim_1.verbose = True
    sim.push(sim_1)

    sim_15 = LFPy_util.sims.MultiSpike()
    sim_15.set_name('freq_15')
    sim_15.run_param['pptype'] = 'ISyn'
    sim_15.run_param['threshold'] = 4
    sim_15.run_param['delay'] = 100
    sim_15.run_param['duration'] = 1000
    sim_15.run_param['spikes'] = 15
    sim_15.verbose = True
    sim.push(sim_15)

    return sim

if __name__ == '__main__':

    # Download models if they do not exist.
    blue_brain.download_all_models(dir_model)

    # Names of the neurons that also match the model folders.
    neurons = []
    # neurons.append('L23_PC_cADpyr229_1')
    # neurons.append('L4_PC_cADpyr230_1')
    # neurons.append('L5_STPC_cADpyr232_1')
    # neurons.append('L5_STPC_cADpyr232_2')
    # neurons.append('L5_STPC_cADpyr232_3')
    # neurons.append('L5_STPC_cADpyr232_4')
    # neurons.append('L5_STPC_cADpyr232_5')
    neurons.append('L5_TTPC1_cADpyr232_1')
    # neurons.append('L5_TTPC2_cADpyr232_1')
    # neurons.append('L5_UTPC_cADpyr232_1')
    # neurons.append('L5_UTPC_cADpyr232_2')
    # neurons.append('L5_UTPC_cADpyr232_3')
    # neurons.append('L5_UTPC_cADpyr232_4')
    # neurons.append('L5_UTPC_cADpyr232_5')
    # neurons.append('L6_BPC_cADpyr231_1')
    # neurons.append('L6_IPC_cADpyr231_1')
    # neurons.append('L6_TPC_L1_cADpyr231_1')
    # neurons.append('L6_TPC_L4_cADpyr231_1')
    # neurons.append('L6_UTPC_cADpyr231_1')

    # neurons.append('L5_LBC_bAC217_1')
    # neurons.append('L5_LBC_cACint209_1')
    # neurons.append('L5_LBC_cIR216_1')
    # neurons.append('L5_LBC_cNAC187_1')
    # neurons.append('L5_LBC_cSTUT189_1')
    # neurons.append('L5_LBC_dNAC222_1')
    # neurons.append('L5_LBC_dSTUT214_1')
    # neurons.append('L5_LBC_dSTUT214_2')
    # neurons.append('L5_LBC_dSTUT214_3')
    # neurons.append('L5_LBC_dSTUT214_4')
    # neurons.append('L5_LBC_dSTUT214_5')

    # neurons.append('L5_LBC_bAC217_1')
    # neurons.append('L5_TTPC2_cADpyr232_1')
    # neurons.append('L5_NBC_cNAC187_1')
    # neurons.append('L23_LBC_cSTUT189_1')
    # neurons.append('L23_NBC_cNAC187_1')
    # neurons.append('L23_PC_cADpyr229_1')

    # neurons.append('L5_LBC_dSTUT214_2')
    # neurons.append('L5_LBC_dSTUT214_3')
    # neurons.append('L5_LBC_dSTUT214_4')
    # neurons.append('L5_LBC_dSTUT214_5')

    # Compile and load the extra mod file(s). The ISyn electrode.
    mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod')
    LFPy_util.other.nrnivmodl(mod_dir, suppress=True)

    # Simulation
    simm = LFPy_util.SimulatorManager()
    simm.concurrent_neurons = 4
    simm.set_neuron_names(neurons)
    simm.set_sim_load_func(get_simulator)
    print simm
    # simm.simulate()
    simm.plot()

