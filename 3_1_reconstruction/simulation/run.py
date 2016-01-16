import LFPy
import LFPy_util
import os
import sys
import numpy as np
import neuron

dir_project = os.path.dirname(os.path.realpath(__file__))
dir_res = os.path.join(dir_project,"res")
dir_neurons = dir_project

# Configure simulation objects.
sim_grid            = LFPy_util.sims.Grid()
sim_disc_elec       = LFPy_util.sims.DiscElectrodes()
sim_morph           = LFPy_util.sims.Morphology()
sim_intra           = LFPy_util.sims.Intracellular()
sim_disc_elec.plot_detailed = True
sim_disc_elec.run_param['threshold'] = 1

cellParameters = {
    'morphology' : os.path.join(dir_res,'morphology/L5_Mainen96_LFPy.hoc'),
    'rm' : 30000,               # membrane resistance
    'cm' : 1.0,                 # membrane capacitance
    'Ra' : 150,                 # axial resistance
    'v_init' : -0,             # initial crossmembrane potential
    'e_pas' : -0,              # reversal potential passive mechs
    'passive' : True,           # switch on passive mechs
    'timeres_NEURON' : 2**-5,   # dt of LFP and NEURON simulation.
    'timeres_python' : 2**-5,
    'tstartms' : -00,           #start time, recorders start at t=0
    'tstopms' : 16.7,             #stop time of simulation
    'pt3d' : True,
}


#Initialize cell instance, using the LFPy.Cell class
cell = LFPy.Cell(**cellParameters)

path = os.path.join(dir_res,'cs_ap.js')
param = LFPy_util.other.load_kwargs_json(path)

# Play vectors back into all soma segments.
v_vec = np.array(param['v_vec'])
t_vec = np.array(param['t_vec'])
v_vec = neuron.h.Vector(v_vec)
t_vec = neuron.h.Vector(t_vec)
for idx, sec in enumerate(cell.somalist):
    for seg in sec:
        v_vec.play(seg._ref_v, t_vec)

# Engage the simulation helper
sh = LFPy_util.SimulationHelper()
sh.set_cell(cell)
sh.set_dir_neurons(dir_neurons)
sh.set_neuron_name("L5_Mainen96")
print sh

# Find the principal component axes and rotate cell.
axes = LFPy_util.data_extraction.findMajorAxes()
LFPy_util.rotation.alignCellToAxes(cell,axes[0],axes[1])

# sh.push(sim_grid,True)
sh.push(sim_disc_elec,False)
# sh.push(sim_morph,True)
# sh.push(sim_intra,True)

sh.simulate()
sh.plot()





















