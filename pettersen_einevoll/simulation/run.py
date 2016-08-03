import LFPy
import LFPy_util
import os
import sys
import numpy as np
import neuron

dir_project = os.path.dirname(os.path.realpath(__file__))
dir_res = os.path.join(dir_project, "res")
dir_neurons = dir_project

cellParameters = {
    'morphology': os.path.join(dir_res, 'morphology/L5_Mainen96_LFPy.hoc'),
    'rm': 30000,  # membrane resistance
    'cm': 1.0,  # membrane capacitance
    'Ra': 150,  # axial resistance
    'v_init': -0,  # initial crossmembrane potential
    'e_pas': -0,  # reversal potential passive mechs
    'passive': True,  # switch on passive mechs
    'timeres_NEURON': 2** -5,  # dt of LFP and NEURON simulation.
    'timeres_python': 2** -5,
    'tstartms': 0,  #start time, recorders start at t=0
    'tstopms': 16.7,  #stop time of simulation
    'pt3d': True,
}

# Path to the action potential.
path = os.path.join(dir_res, 'cs_ap.js')
param = LFPy_util.other.load_kwargs_json(path)

v_vec = np.array(param['v_vec'])
t_vec = np.array(param['t_vec'])
v_vec = neuron.h.Vector(v_vec)
t_vec = neuron.h.Vector(t_vec)

#Initialize cell instance, using the LFPy.Cell class
def get_cell(neuron_name):
    cell = LFPy.Cell(**cellParameters)

    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])

    # Play vectors back into all soma segments.
    for idx, sec in enumerate(cell.somalist):
        for seg in sec:
            v_vec.play(seg._ref_v, t_vec)

    return cell

# Engage the simulation helper.
sh = LFPy_util.Simulator()
sh.set_cell_load_func(get_cell)
sh.set_output_dir(dir_neurons)
sh.set_neuron_name("L5_Mainen96")
print sh

# Configure simulation objects.
sim_intra = LFPy_util.sims.Intracellular()
sim_intra.process_param['padding_factor'] = 1
sh.push(sim_intra)

sim_morph = LFPy_util.sims.Morphology()
sh.push(sim_morph)

sim_disc = LFPy_util.sims.DiscXY()
sim_disc.run_param['n'] = 11
sim_disc.run_param['n_phi'] = 36
sim_disc.run_param['R'] = 120
sim_disc.run_param['R_0'] = 20
sim_disc.process_param['width_II_thresh'] = 0.25
sim_disc.plot_param['plot_detailed'] = True
sh.push(sim_disc)
sim_disc = LFPy_util.sims.DiscXY()
sim_disc.set_name('disc_0375')
sim_disc.run_param['n'] = 11
sim_disc.run_param['n_phi'] = 36
sim_disc.run_param['R'] = 120
sim_disc.run_param['R_0'] = 20
sim_disc.process_param['width_II_thresh'] = 0.375
sim_disc.plot_param['plot_detailed'] = True
sh.push(sim_disc)


sh.simulate()
sh.plot()
