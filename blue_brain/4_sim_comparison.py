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
dir_output = os.path.join(dir_current, "4_sim_comparison")

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

    sim_sweep = LFPy_util.sims.CurrentSweep()
    sim_sweep.run_param['pptype'] = 'ISyn'
    sim_sweep.run_param['duration'] = 1000
    sim_sweep.run_param['delay'] = 100
    sim_sweep.run_param['sweeps'] = 16
    sim_sweep.run_param['processes'] = 4
    sim_sweep.run_param['n_elec'] = 2
    sim_sweep.run_param['seed'] = 1
    sim_sweep.plot_param['use_tex'] = False
    if 'L5_TTPC1_cADpyr232_1' in neuron_name:
        sim_sweep.run_param['amp_start'] = 0.213
        sim_sweep.run_param['amp_end'] = 0.931

    sim.push(sim_sweep)

    sim_morph = LFPy_util.sims.Morphology()
    sim.push(sim_morph)

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
    simm.concurrent_neurons = 2
    simm.set_neuron_names(neurons)
    simm.set_sim_load_func(get_simulator)
    print simm
    simm.simulate()
    simm.plot()

