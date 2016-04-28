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
DIR_OUTPUT = os.path.join(DIR_CURRENT, "4_3_simulation_0")

def get_cell(neuron_name):
    """
    Function that loads a cell using the name of the neuron.
    """
    nrn_full = os.path.join(DIR_MODELS, neuron_name)
    cell_list = blue_brain.load_model(nrn_full, suppress=True)
    cell = cell_list[0]
    cell.tstartms = 0
    cell.tstopms = 500
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
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
    sim_multi.run_param['delay'] = 100
    sim_multi.run_param['duration'] = 400
    sim_multi.run_param['spikes'] = 3
    sim_multi.run_param['init_amp'] = 0.30
    sim_multi.verbose = True
    # sim.push(sim_multi, False)

    sim_sphere = LFPy_util.sims.SphereRand()
    sim_sphere.run_param['N'] = 500
    sim_sphere.run_param['R'] = 60
    sim_sphere.run_param['seed'] = np.random.randint(1e6)
    sim_sphere.process_param['spike_to_measure'] = 2
    sim_sphere.process_param['assert_width'] = True
    # sim.push(sim_sphere)

    sim_sphere_filt = LFPy_util.sims.SphereRandFilt()
    sim_sphere_filt.simulate = False
    sim_sphere.process_param['spike_to_measure'] = 2
    sim_sphere.process_param['assert_width'] = True
    # sim.push(sim_sphere_filt)

    sim_morph = LFPy_util.sims.Morphology()
    # sim.push(sim_morph)

    sim_width = LFPy_util.sims.SpikeWidthDef()
    sim_width.run_param['N'] = 10
    sim_width.process_param['spike_to_measure'] = 2
    # sim.push(sim_width)

    sim_width_filt = LFPy_util.sims.SpikeWidthDefFilt()
    sim_width_filt.process_param['spike_to_measure'] = 2
    sim_width_filt.simulate = False
    # sim.push(sim_width_filt)

    sim_width_lfilt = LFPy_util.sims.SpikeWidthDefFilt()
    sim_width_lfilt.process_param['spike_to_measure'] = 2
    sim_width_lfilt.process_param['filter'] = 'lfilter'
    sim_width_lfilt.process_param['freq_low'] = 0.05
    sim_width_lfilt.simulate = False
    sim_width_lfilt.name += 'left'
    sim.push(sim_width_lfilt)
    return sim

if __name__ == '__main__':
    # Download models if they do not exist.
    blue_brain.download_all_models(DIR_MODELS)

    # Names of the neurons that also match the model folders.
    neurons = []
    # neurons.append('L5_LBC_dSTUT214_1')
    # neurons.append('L5_LBC_dSTUT214_2')
    # neurons.append('L5_LBC_dSTUT214_3')
    # neurons.append('L5_LBC_dSTUT214_4')
    # neurons.append('L5_LBC_dSTUT214_5')
    # neurons.append('L5_NBC_cNAC187_1')
    # neurons.append('L5_NBC_cNAC187_2')
    # neurons.append('L5_NBC_cNAC187_3')
    # neurons.append('L5_NBC_cNAC187_4')
    # neurons.append('L5_NBC_cNAC187_5')
    neurons.append('L5_TTPC2_cADpyr232_1')
    # neurons.append('L5_TTPC2_cADpyr232_2')
    # neurons.append('L5_TTPC2_cADpyr232_3')
    # neurons.append('L5_TTPC2_cADpyr232_4')
    # neurons.append('L5_TTPC2_cADpyr232_5')

    # Compile and load the extra mod file(s). The ISyn electrode.
    mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod')
    LFPy_util.other.nrnivmodl(mod_dir, suppress=True)

    # Simulation
    simm = LFPy_util.SimulatorManager()
    simm.concurrent_neurons = 8
    simm.set_neuron_names(neurons)
    simm.set_sim_load_func(get_simulator)
    print simm
    # simm.simulate()
    simm.plot()

