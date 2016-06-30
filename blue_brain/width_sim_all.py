"""
Calculate the width and amp dependency in relation to distance from
soma for TTPC, LBC and NBC neurons of the same e-type but different m-type.
"""
# pylint: disable=invalid-name

import os
from glob import glob
import LFPy_util
import blue_brain
import copy
import numpy as np

# Gather directory paths.
DIR_MODELS = blue_brain.DIR_MODELS
DIR_CURRENT = os.path.dirname(os.path.realpath(__file__))
DIR_OUTPUT = os.path.join(DIR_CURRENT, "width_sim_all")

def get_cell(neuron_name):
    """
    Function that loads a cell using the name of the neuron.
    """
    nrn_full = os.path.join(DIR_MODELS, neuron_name)
    cell_list = blue_brain.load_model(nrn_full, suppress=True)
    cell = cell_list[0]
    cell.tstartms = 0
    cell.tstopms = 200
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()

    # A quickfix for flipping axes so the neurons lie in
    # the same direction. Not a very elegant solution.
    for i, axis in enumerate(axes):
        if axis.sum() < 0:
            axes[i] = -axis
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    return cell

def get_simulator(neuron_name):
    """
    Define the simulation. Which simulations to use and the parameters.
    """
    sim = LFPy_util.Simulator()
    sim.set_cell_load_func(get_cell)
    sim.set_output_dir(DIR_OUTPUT)
    sim.set_neuron_name(neuron_name)

    # Simulation objects.
    sim_multi = LFPy_util.sims.MultiSpike()
    sim_multi.run_param['pptype'] = 'ISyn'
    sim_multi.run_param['threshold'] = 4
    sim_multi.run_param['delay'] = 000
    sim_multi.run_param['duration'] = 200
    sim_multi.run_param['spikes'] = 3
    if 'TTPC' in neuron_name:
        sim_multi.run_param['init_amp'] = 0.50
    elif 'NBC' in neuron_name:
        sim_multi.run_param['init_amp'] = 0.05
    else:
        sim_multi.run_param['init_amp'] = 0.05
    sim_multi.verbose = True
    sim.push(sim_multi, False)

    sim_sphere = LFPy_util.sims.SphereRand()
    sim_sphere.run_param['sigma'] = 0.3
    sim_sphere.run_param['N'] = 1000
    sim_sphere.run_param['R'] = 60
    sim_sphere.run_param['seed'] = np.random.randint(1e5) #4321
    sim_sphere.process_param['spike_to_measure'] = 2
    sim_sphere.process_param['assert_width'] = True
    sim_sphere.plot_param['use_tex'] = False
    sim.push(sim_sphere)

    sim_morph = LFPy_util.sims.Morphology()
    sim_morph.plot_param['use_tex'] = False
    sim.push(sim_morph)

    return sim

if __name__ == '__main__':
    # Download models if they do not exist.
    blue_brain.download_all_models(DIR_MODELS)

    # Names of the neurons that also match the model folders.
    neurons = []
    neurons.append('L5_BP_bAC217_1')
    neurons.append('L5_BP_bAC217_2')
    neurons.append('L5_BP_bAC217_3')
    neurons.append('L5_BP_bAC217_4')
    neurons.append('L5_BP_bAC217_5')
    neurons.append('L5_BP_bIR215_1')
    neurons.append('L5_BP_bIR215_2')
    neurons.append('L5_BP_bIR215_3')
    neurons.append('L5_BP_bIR215_4')
    neurons.append('L5_BP_bIR215_5')
    neurons.append('L5_BP_bNAC219_1')
    neurons.append('L5_BP_bNAC219_2')
    neurons.append('L5_BP_bNAC219_3')
    neurons.append('L5_BP_bNAC219_4')
    neurons.append('L5_BP_bNAC219_5')
    neurons.append('L5_BP_cACint209_1')
    neurons.append('L5_BP_cACint209_2')
    neurons.append('L5_BP_cACint209_3')
    neurons.append('L5_BP_cACint209_4')
    neurons.append('L5_BP_cACint209_5')
    neurons.append('L5_BP_cNAC187_1')
    neurons.append('L5_BP_cNAC187_2')
    neurons.append('L5_BP_cNAC187_3')
    neurons.append('L5_BP_cNAC187_4')
    neurons.append('L5_BP_cNAC187_5')
    neurons.append('L5_BP_dSTUT214_1')
    neurons.append('L5_BP_dSTUT214_2')
    neurons.append('L5_BP_dSTUT214_3')
    neurons.append('L5_BP_dSTUT214_4')
    neurons.append('L5_BP_dSTUT214_5')
    neurons.append('L5_BTC_bAC217_1')
    neurons.append('L5_BTC_bAC217_2')
    neurons.append('L5_BTC_bAC217_3')
    neurons.append('L5_BTC_bAC217_4')
    neurons.append('L5_BTC_bAC217_5')
    neurons.append('L5_BTC_cACint209_1')
    neurons.append('L5_BTC_cACint209_2')
    neurons.append('L5_BTC_cACint209_3')
    neurons.append('L5_BTC_cACint209_4')
    neurons.append('L5_BTC_cACint209_5')
    neurons.append('L5_BTC_cNAC187_1')
    neurons.append('L5_BTC_cNAC187_2')
    neurons.append('L5_BTC_cNAC187_3')
    neurons.append('L5_BTC_cNAC187_4')
    neurons.append('L5_BTC_cNAC187_5')
    neurons.append('L5_ChC_cACint209_1')
    neurons.append('L5_ChC_cACint209_2')
    neurons.append('L5_ChC_cACint209_3')
    neurons.append('L5_ChC_cACint209_4')
    neurons.append('L5_ChC_cACint209_5')
    neurons.append('L5_ChC_cNAC187_1')
    neurons.append('L5_ChC_cNAC187_2')
    neurons.append('L5_ChC_cNAC187_3')
    neurons.append('L5_ChC_cNAC187_4')
    neurons.append('L5_ChC_cNAC187_5')
    neurons.append('L5_ChC_dNAC222_1')
    neurons.append('L5_ChC_dNAC222_2')
    neurons.append('L5_ChC_dNAC222_3')
    neurons.append('L5_ChC_dNAC222_4')
    neurons.append('L5_ChC_dNAC222_5')
    neurons.append('L5_DBC_bAC217_1')
    neurons.append('L5_DBC_bAC217_2')
    neurons.append('L5_DBC_bAC217_3')
    neurons.append('L5_DBC_bAC217_4')
    neurons.append('L5_DBC_bAC217_5')
    neurons.append('L5_DBC_bIR215_1')
    neurons.append('L5_DBC_bIR215_2')
    neurons.append('L5_DBC_bIR215_3')
    neurons.append('L5_DBC_bIR215_4')
    neurons.append('L5_DBC_bIR215_5')
    neurons.append('L5_DBC_bNAC219_1')
    neurons.append('L5_DBC_bNAC219_2')
    neurons.append('L5_DBC_bNAC219_3')
    neurons.append('L5_DBC_bNAC219_4')
    neurons.append('L5_DBC_bNAC219_5')
    neurons.append('L5_DBC_bSTUT213_1')
    neurons.append('L5_DBC_bSTUT213_2')
    neurons.append('L5_DBC_bSTUT213_3')
    neurons.append('L5_DBC_bSTUT213_4')
    neurons.append('L5_DBC_bSTUT213_5')
    neurons.append('L5_DBC_cACint209_1')
    neurons.append('L5_DBC_cACint209_2')
    neurons.append('L5_DBC_cACint209_3')
    neurons.append('L5_DBC_cACint209_4')
    neurons.append('L5_DBC_cACint209_5')
    neurons.append('L5_DBC_cIR216_1')
    neurons.append('L5_DBC_cIR216_2')
    neurons.append('L5_DBC_cIR216_3')
    neurons.append('L5_DBC_cIR216_4')
    neurons.append('L5_DBC_cIR216_5')
    neurons.append('L5_DBC_cNAC187_1')
    neurons.append('L5_DBC_cNAC187_2')
    neurons.append('L5_DBC_cNAC187_3')
    neurons.append('L5_DBC_cNAC187_4')
    neurons.append('L5_DBC_cNAC187_5')
    neurons.append('L5_LBC_bAC217_1')
    neurons.append('L5_LBC_bAC217_2')
    neurons.append('L5_LBC_bAC217_3')
    neurons.append('L5_LBC_bAC217_4')
    neurons.append('L5_LBC_bAC217_5')
    neurons.append('L5_LBC_cACint209_1')
    neurons.append('L5_LBC_cACint209_2')
    neurons.append('L5_LBC_cACint209_3')
    neurons.append('L5_LBC_cACint209_4')
    neurons.append('L5_LBC_cACint209_5')
    neurons.append('L5_LBC_cIR216_1')
    neurons.append('L5_LBC_cIR216_2')
    neurons.append('L5_LBC_cIR216_3')
    neurons.append('L5_LBC_cIR216_4')
    neurons.append('L5_LBC_cIR216_5')
    neurons.append('L5_LBC_cNAC187_1')
    neurons.append('L5_LBC_cNAC187_2')
    neurons.append('L5_LBC_cNAC187_3')
    neurons.append('L5_LBC_cNAC187_4')
    neurons.append('L5_LBC_cNAC187_5')
    neurons.append('L5_LBC_cSTUT189_1')
    neurons.append('L5_LBC_cSTUT189_2')
    neurons.append('L5_LBC_cSTUT189_3')
    neurons.append('L5_LBC_cSTUT189_4')
    neurons.append('L5_LBC_cSTUT189_5')
    neurons.append('L5_LBC_dNAC222_1')
    neurons.append('L5_LBC_dNAC222_2')
    neurons.append('L5_LBC_dNAC222_3')
    neurons.append('L5_LBC_dNAC222_4')
    neurons.append('L5_LBC_dNAC222_5')
    neurons.append('L5_LBC_dSTUT214_1')
    neurons.append('L5_LBC_dSTUT214_2')
    neurons.append('L5_LBC_dSTUT214_3')
    neurons.append('L5_LBC_dSTUT214_4')
    neurons.append('L5_LBC_dSTUT214_5')
    neurons.append('L5_MC_bAC217_1')
    neurons.append('L5_MC_bAC217_2')
    neurons.append('L5_MC_bAC217_3')
    neurons.append('L5_MC_bAC217_4')
    neurons.append('L5_MC_bAC217_5')
    neurons.append('L5_MC_bIR215_1')
    neurons.append('L5_MC_bIR215_2')
    neurons.append('L5_MC_bIR215_3')
    neurons.append('L5_MC_bIR215_4')
    neurons.append('L5_MC_bIR215_5')
    neurons.append('L5_MC_bSTUT213_1')
    neurons.append('L5_MC_bSTUT213_2')
    neurons.append('L5_MC_bSTUT213_3')
    neurons.append('L5_MC_bSTUT213_4')
    neurons.append('L5_MC_bSTUT213_5')
    neurons.append('L5_MC_cACint209_1')
    neurons.append('L5_MC_cACint209_2')
    neurons.append('L5_MC_cACint209_3')
    neurons.append('L5_MC_cACint209_4')
    neurons.append('L5_MC_cACint209_5')
    neurons.append('L5_MC_cNAC187_1')
    neurons.append('L5_MC_cNAC187_2')
    neurons.append('L5_MC_cNAC187_3')
    neurons.append('L5_MC_cNAC187_4')
    neurons.append('L5_MC_cNAC187_5')
    neurons.append('L5_MC_cSTUT189_1')
    neurons.append('L5_MC_cSTUT189_2')
    neurons.append('L5_MC_cSTUT189_3')
    neurons.append('L5_MC_cSTUT189_4')
    neurons.append('L5_MC_cSTUT189_5')
    neurons.append('L5_MC_dNAC222_1')
    neurons.append('L5_MC_dNAC222_2')
    neurons.append('L5_MC_dNAC222_3')
    neurons.append('L5_MC_dNAC222_4')
    neurons.append('L5_MC_dNAC222_5')
    neurons.append('L5_NBC_bAC217_1')
    neurons.append('L5_NBC_bAC217_2')
    neurons.append('L5_NBC_bAC217_3')
    neurons.append('L5_NBC_bAC217_4')
    neurons.append('L5_NBC_bAC217_5')
    neurons.append('L5_NBC_bIR215_1')
    neurons.append('L5_NBC_bIR215_2')
    neurons.append('L5_NBC_bIR215_3')
    neurons.append('L5_NBC_bIR215_4')
    neurons.append('L5_NBC_bIR215_5')
    neurons.append('L5_NBC_bSTUT213_1')
    neurons.append('L5_NBC_bSTUT213_2')
    neurons.append('L5_NBC_bSTUT213_3')
    neurons.append('L5_NBC_bSTUT213_4')
    neurons.append('L5_NBC_bSTUT213_5')
    neurons.append('L5_NBC_cACint209_1')
    neurons.append('L5_NBC_cACint209_2')
    neurons.append('L5_NBC_cACint209_3')
    neurons.append('L5_NBC_cACint209_4')
    neurons.append('L5_NBC_cACint209_5')
    neurons.append('L5_NBC_cIR216_1')
    neurons.append('L5_NBC_cIR216_2')
    neurons.append('L5_NBC_cIR216_3')
    neurons.append('L5_NBC_cIR216_4')
    neurons.append('L5_NBC_cIR216_5')
    neurons.append('L5_NBC_cNAC187_1')
    neurons.append('L5_NBC_cNAC187_2')
    neurons.append('L5_NBC_cNAC187_3')
    neurons.append('L5_NBC_cNAC187_4')
    neurons.append('L5_NBC_cNAC187_5')
    neurons.append('L5_NBC_cSTUT189_1')
    neurons.append('L5_NBC_cSTUT189_2')
    neurons.append('L5_NBC_cSTUT189_3')
    neurons.append('L5_NBC_cSTUT189_4')
    neurons.append('L5_NBC_cSTUT189_5')
    neurons.append('L5_NBC_dSTUT214_1')
    neurons.append('L5_NBC_dSTUT214_2')
    neurons.append('L5_NBC_dSTUT214_3')
    neurons.append('L5_NBC_dSTUT214_4')
    neurons.append('L5_NBC_dSTUT214_5')
    neurons.append('L5_NGC_bNAC219_1')
    neurons.append('L5_NGC_bNAC219_2')
    neurons.append('L5_NGC_bNAC219_3')
    neurons.append('L5_NGC_bNAC219_4')
    neurons.append('L5_NGC_bNAC219_5')
    neurons.append('L5_NGC_cACint209_1')
    neurons.append('L5_NGC_cACint209_2')
    neurons.append('L5_NGC_cACint209_3')
    neurons.append('L5_NGC_cACint209_4')
    neurons.append('L5_NGC_cACint209_5')
    neurons.append('L5_NGC_cNAC187_1')
    neurons.append('L5_NGC_cNAC187_2')
    neurons.append('L5_NGC_cNAC187_3')
    neurons.append('L5_NGC_cNAC187_4')
    neurons.append('L5_NGC_cNAC187_5')
    neurons.append('L5_NGC_cSTUT189_1')
    neurons.append('L5_NGC_cSTUT189_2')
    neurons.append('L5_NGC_cSTUT189_3')
    neurons.append('L5_NGC_cSTUT189_4')
    neurons.append('L5_NGC_cSTUT189_5')
    neurons.append('L5_SBC_bNAC219_1')
    neurons.append('L5_SBC_bNAC219_2')
    neurons.append('L5_SBC_bNAC219_3')
    neurons.append('L5_SBC_bNAC219_4')
    neurons.append('L5_SBC_bNAC219_5')
    neurons.append('L5_SBC_cACint209_1')
    neurons.append('L5_SBC_cACint209_2')
    neurons.append('L5_SBC_cACint209_3')
    neurons.append('L5_SBC_cACint209_4')
    neurons.append('L5_SBC_cACint209_5')
    neurons.append('L5_SBC_dNAC222_1')
    neurons.append('L5_SBC_dNAC222_2')
    neurons.append('L5_SBC_dNAC222_3')
    neurons.append('L5_SBC_dNAC222_4')
    neurons.append('L5_SBC_dNAC222_5')
    neurons.append('L5_STPC_cADpyr232_1')
    neurons.append('L5_STPC_cADpyr232_2')
    neurons.append('L5_STPC_cADpyr232_3')
    neurons.append('L5_STPC_cADpyr232_4')
    neurons.append('L5_STPC_cADpyr232_5')
    neurons.append('L5_TTPC1_cADpyr232_1')
    neurons.append('L5_TTPC1_cADpyr232_2')
    neurons.append('L5_TTPC1_cADpyr232_3')
    neurons.append('L5_TTPC1_cADpyr232_4')
    neurons.append('L5_TTPC1_cADpyr232_5')
    neurons.append('L5_TTPC2_cADpyr232_1')
    neurons.append('L5_TTPC2_cADpyr232_2')
    neurons.append('L5_TTPC2_cADpyr232_3')
    neurons.append('L5_TTPC2_cADpyr232_4')
    neurons.append('L5_TTPC2_cADpyr232_5')
    neurons.append('L5_UTPC_cADpyr232_1')
    neurons.append('L5_UTPC_cADpyr232_2')
    neurons.append('L5_UTPC_cADpyr232_3')
    neurons.append('L5_UTPC_cADpyr232_4')
    neurons.append('L5_UTPC_cADpyr232_5')

    # Ols list                  
    # neurons.append('L5_LBC_cNAC187_1')
    # neurons.append('L5_LBC_cNAC187_2')
    # neurons.append('L5_LBC_cNAC187_3')
    # neurons.append('L5_LBC_cNAC187_4')
    # neurons.append('L5_LBC_cNAC187_5')

    # neurons.append('L5_LBC_dSTUT214_1')
    # neurons.append('L5_LBC_dSTUT214_2')
    # neurons.append('L5_LBC_dSTUT214_3')
    # neurons.append('L5_LBC_dSTUT214_4')
    # neurons.append('L5_LBC_dSTUT214_5')

    # neurons.append('L5_LBC_bAC217_1')
    # neurons.append('L5_LBC_bAC217_2')
    # neurons.append('L5_LBC_bAC217_3')
    # neurons.append('L5_LBC_bAC217_4')
    # neurons.append('L5_LBC_bAC217_5')

    # neurons.append('L5_LBC_cACint209_1')
    # neurons.append('L5_LBC_cACint209_2')
    # neurons.append('L5_LBC_cACint209_3')
    # neurons.append('L5_LBC_cACint209_4')
    # neurons.append('L5_LBC_cACint209_5')

    # neurons.append('L5_NBC_cNAC187_1')
    # neurons.append('L5_NBC_cNAC187_2')
    # neurons.append('L5_NBC_cNAC187_3')
    # neurons.append('L5_NBC_cNAC187_4')
    # neurons.append('L5_NBC_cNAC187_5')

    # neurons.append('L5_NBC_bAC217_1')
    # neurons.append('L5_NBC_bAC217_2')
    # neurons.append('L5_NBC_bAC217_3')
    # neurons.append('L5_NBC_bAC217_4')
    # neurons.append('L5_NBC_bAC217_5')

    # neurons.append('L5_NBC_bIR215_1')
    # neurons.append('L5_NBC_bIR215_2')
    # neurons.append('L5_NBC_bIR215_3')
    # neurons.append('L5_NBC_bIR215_4')
    # neurons.append('L5_NBC_bIR215_5')

    # neurons.append('L5_NBC_dSTUT214_1')
    # neurons.append('L5_NBC_dSTUT214_2')
    # neurons.append('L5_NBC_dSTUT214_3')
    # neurons.append('L5_NBC_dSTUT214_4')
    # neurons.append('L5_NBC_dSTUT214_5')

    # neurons.append('L5_TTPC1_cADpyr232_1')
    # neurons.append('L5_TTPC1_cADpyr232_2')
    # neurons.append('L5_TTPC1_cADpyr232_3')
    # neurons.append('L5_TTPC1_cADpyr232_4')
    # neurons.append('L5_TTPC1_cADpyr232_5')

    # neurons.append('L5_TTPC2_cADpyr232_1')
    # neurons.append('L5_TTPC2_cADpyr232_2')
    # neurons.append('L5_TTPC2_cADpyr232_3')
    # neurons.append('L5_TTPC2_cADpyr232_4')
    # neurons.append('L5_TTPC2_cADpyr232_5')

    # neurons.append('L5_UTPC_cADpyr232_1')
    # neurons.append('L5_UTPC_cADpyr232_2')
    # neurons.append('L5_UTPC_cADpyr232_3')
    # neurons.append('L5_UTPC_cADpyr232_4')
    # neurons.append('L5_UTPC_cADpyr232_5')

    # neurons.append('L5_STPC_cADpyr232_1')
    # neurons.append('L5_STPC_cADpyr232_2')
    # neurons.append('L5_STPC_cADpyr232_3')
    # neurons.append('L5_STPC_cADpyr232_4')
    # neurons.append('L5_STPC_cADpyr232_5')

    # Compile and load the extra mod file(s). The ISyn electrode.
    mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod')
    LFPy_util.other.nrnivmodl(mod_dir, suppress=True)

    # Simulation
    simm = LFPy_util.SimulatorManager()
    simm.concurrent_neurons = 8
    simm.set_neuron_names(neurons)
    simm.set_sim_load_func(get_simulator)
    print simm
    simm.simulate()
    # simm.plot()

