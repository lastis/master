# Simulation: Gather different data about single neurons.
import blue_brain
import LFPy_util

import os
from glob import glob
from multiprocessing import Process
import sys

# Gather directory paths. 
model_dir = blue_brain.model_dir
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current,"neurons")

# Download if they do not exist.
blue_brain.download_all_models(model_dir)

# Load pyramidal cells in L5.
os.chdir(model_dir)
PC = glob('L5_*PC*')
NBC = glob('L5_*NBC*')
SBC = glob('L5_*SBC*')
DBC = glob('L5_*DBC*')

# group_labels = ['SBC', 'DBC']
# neurons_grouped = [SBC,DBC]
# group_labels = ['PC', 'NBC', 'SBC', 'DBC']
# neurons_grouped = [PC,NBC,SBC,DBC]
# group_labels = ['PC', 'NBC']
# neurons_grouped = [PC,NBC]
group_labels = ['NBC']
neurons_grouped = [NBC]

# Compile and load the extra mod file(s).
mod_dir = os.path.join(blue_brain.res_dir,'extra_mod/')
LFPy_util.nrnivmodl(mod_dir)


# Configure simulation objects.
sim_grid            = LFPy_util.sims.Grid()
sim_single_spike    = LFPy_util.sims.SingleSpike()
sim_disc_elec       = LFPy_util.sims.DiscElectrodes()
sim_morph           = LFPy_util.sims.Morphology()
sim_intra           = LFPy_util.sims.Intracellular()
sim_single_spike.run_param['pptype'] = 'ISyn'

for neurons in neurons_grouped:
    processes = []
    for cnt, nrn in enumerate(neurons):
        if cnt > 0: break
        nrn_full = os.path.join(model_dir,nrn)
        # Load cell objects from bluebrain.
        cell_list = blue_brain.load_model(nrn_full)
        # Assume only one morphology of each neuron.
        cell = cell_list[0]

        sh = LFPy_util.SimulationHelper()
        sh.set_cell(cell)
        sh.set_dir_neurons(dir_neurons)
        sh.set_neuron_name(nrn)
        print sh

        # Find the principal component axes and rotate cell.
        axes = LFPy_util.data_extraction.findMajorAxes()
        LFPy_util.rotation.alignCellToAxes(cell,axes[0],axes[1])

        sh.push(sim_single_spike,False)
        sh.push(sim_grid,True)
        sh.push(sim_disc_elec,True)
        sh.push(sim_morph,True)
        sh.push(sim_intra,True)

        sh.simulate()
        sh.plot()





















