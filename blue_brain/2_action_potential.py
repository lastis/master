"""
Calculate the width and amp dependency in relation to distance from
soma for TTPC, LBC and NBC neurons of the same e-type but different m-type.
"""
# pylint: disable=invalid-name

import os
import LFPy_util
import blue_brain
import numpy as np

# Gather directory paths.
DIR_MODELS = blue_brain.DIR_MODELS
DIR_CURRENT = os.path.dirname(os.path.realpath(__file__))
DIR_OUTPUT = os.path.join(DIR_CURRENT, "2_action_potential")

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
    sim_multi.run_param['delay'] = 50
    sim_multi.run_param['duration'] = 2
    sim_multi.run_param['spikes'] = 1
    if 'TTPC' in neuron_name:
        sim_multi.run_param['init_amp'] = 2.0
    else:
        sim_multi.run_param['init_amp'] = 0.7
    sim_multi.verbose = True
    sim.push(sim_multi, False)

    sim_width = LFPy_util.sims.SpikeWidthDef()
    sim_width.run_param['N'] = 1
    sim_width.process_param['pre_dur'] = 3.0
    sim_width.process_param['post_dur'] = 7.0
    sim.push(sim_width)

    return sim

if __name__ == '__main__':
    # Download models if they do not exist.
    blue_brain.download_all_models(DIR_MODELS)

    # Names of the neurons that also match the model folders.
    neurons = []
    neurons.append('L5_NBC_cNAC187_1')

    # Compile and load the extra mod file(s). The ISyn electrode.
    mod_dir = os.path.join(blue_brain.DIR_RES, 'extra_mod')
    LFPy_util.other.nrnivmodl(mod_dir, suppress=True)

    # Simulation
    simm = LFPy_util.SimulatorManager()
    simm.concurrent_neurons = 5
    simm.set_neuron_names(neurons)
    simm.set_sim_load_func(get_simulator)
    print simm
    simm.simulate()
    simm.plot()

