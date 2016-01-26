import blue_brain
import LFPy_util
import os
from glob import glob

output_dir = "sim_04"
simulate = False
plot = True
# How many neurons from each group to simulate.
nrn_cnt = 1

# Gather directory paths.
dir_model = blue_brain.dir_model
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_neurons = os.path.join(dir_current,output_dir)

# Load pyramidal cells in L5.
os.chdir(dir_model)
TTPC1 = glob('L5_*TTPC1*')[:nrn_cnt]
NBC = glob('L5_*NBC*')[:nrn_cnt]

# Gather neurons to be simulated.
neurons = TTPC1

# Download if they do not exist.
blue_brain.download_all_models(dir_model)

# Compile and load the extra mod file(s).
if simulate:
    mod_dir = os.path.join(blue_brain.dir_res,'extra_mod/')
    LFPy_util.nrnivmodl(mod_dir)
    
# Load cell objects from bluebrain.
def load_func(neuron):
    nrn_full = os.path.join(dir_model,neuron)
    cell_list = blue_brain.load_model(nrn_full)
    cell = cell_list[0]
    return cell

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_func)
sim.set_dir_neurons(dir_neurons)
sim.set_neuron_name(neurons)
sim.simulate = simulate
sim.plot = plot

sim_single_spike    = LFPy_util.sims.SingleSpike()
sim_single_spike.prev_data = sim.get_path_sim_data(sim_single_spike)
sim_single_spike.run_param['pptype'] = 'ISyn'
sim_intra = LFPy_util.sims.Intracellular()
sim_sphere = LFPy_util.sims.SphereElectrodes()
sim_sphere.elec_to_plot = [0,99]
sim_sym = LFPy_util.sims.Symmetry()
sim_sym.plot_detailed = True

# sim.push(sim_single_spike,False)
# sim.push(sim_intra,True)
# sim.push(sim_sphere,True)
sim.push(sim_sym,True)

print sim
sim.run()
