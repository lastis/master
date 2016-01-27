import blue_brain
import LFPy_util
import os
from glob import glob

# Gather directory paths.
dir_model = blue_brain.dir_model
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current,"sim_00_new")

# Download models if they do not exist.
blue_brain.download_all_models(dir_model)

# How many neurons from each group to simulate.
nrn_cnt = 2

# Load pyramidal cells in L5.
os.chdir(dir_model)
TTPC1 = glob('L5_*TTPC1*')[:nrn_cnt]
TTPC2 = glob('L5_*TTPC2*')[:nrn_cnt]
MC = glob('L5_*MC*')[:nrn_cnt]
LBC = glob('L5_*LBC*')[:nrn_cnt]

# Gather neurons to be simulated.
neurons = TTPC1 + TTPC2 + MC + LBC
# neurons = TTPC1 + TTPC2
# neurons = MC + LBC

# Compile and load the extra mod file(s). The ISyn electrode.
mod_dir = os.path.join(blue_brain.dir_res,'extra_mod/')
LFPy_util.nrnivmodl(mod_dir)
    
# Create a load function that loads a cell using the name of the neuron.
def load_func(neuron):
    nrn_full = os.path.join(dir_model,neuron)
    cell_list = blue_brain.load_model(nrn_full)
    cell = cell_list[0]
    # # Find the principal component axes and rotate cell.
    # axes = LFPy_util.data_extraction.findMajorAxes()
    # # Aligns y to axis[0] and x to axis[1]
    # LFPy_util.rotation.alignCellToAxes(cell,axes[0],axes[1])
    return cell

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_func)
sim.set_dir_neurons(dir_neurons)
sim.set_neuron_name(neurons)
sim.simulate = True
sim.plot = False
sim.parallel = False

# Simulation objects.
sim_single_spike    = LFPy_util.sims.SingleSpike()
sim_single_spike.prev_data = sim.get_path_sim_data(sim_single_spike)
sim_single_spike.run_param['pptype'] = 'ISyn'
sim_intra = LFPy_util.sims.Intracellular()
sim_sphere = LFPy_util.sims.SphereElectrodes()
sim_sphere.elec_to_plot = [0,99]
sim_sym = LFPy_util.sims.Symmetry()
sim_morph = LFPy_util.sims.Morphology()

sim.push(sim_single_spike,False)
sim.push(sim_intra,True)
sim.push(sim_sphere,True)
sim.push(sim_sym,True)
sim.push(sim_morph,True)

print sim
sim.run()
