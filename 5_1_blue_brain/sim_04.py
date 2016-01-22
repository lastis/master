import blue_brain
import LFPy_util
import os
import sys
from glob import glob

cores = 1
output_dir = "sim_04"
# How many neurons from each group to simulate.
nrn_cnt = 2

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

# Process command input.
simulate = False
plot = False
for input in sys.argv:
    if input == "run" :
        simulate = True
    if input == "plot" :
        plot = True
if len(sys.argv) == 1:
    simulate = True
    plot = True


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

sh = LFPy_util.SimulationHelper()
sh.set_cell_load_func(load_func)
sh.set_dir_neurons(dir_neurons)
sh.set_neuron_name(neurons)
sh.simulate = simulate
sh.plot = plot

sim_single_spike    = LFPy_util.sims.SingleSpike()
sim_single_spike.prev_data = sh.get_path_sim_data(sim_single_spike)
sim_single_spike.run_param['pptype'] = 'ISyn'
sim_intra           = LFPy_util.sims.Intracellular()

sh.push(sim_single_spike,False)
sh.push(sim_intra,False)

print sh
sh.run()

# # Define a simulation method so different neurons can be run in parallel.
# def run(nrn_full):
#     # Load cell objects from bluebrain.
#     cell_list = blue_brain.load_model(nrn_full)
#     cell = cell_list[0]

#     sh = LFPy_util.SimulationHelper()
#     sh.set_cell(cell)
#     sh.set_dir_neurons(dir_neurons)
#     sh.set_neuron_name(nrn)
#     print sh

#     # Configure simulation objects.
#     sim_single_spike    = LFPy_util.sims.SingleSpike()
#     sim_single_spike.prev_data = sh.get_path_data(sim_single_spike)
#     sim_single_spike.run_param['pptype'] = 'ISyn'
#     sim_morph           = LFPy_util.sims.Morphology()
#     sim_sphere = LFPy_util.sims.SphereElectrodes()

#     # Find the principal component axes and rotate cell.
#     axes = LFPy_util.data_extraction.findMajorAxes()
#     # Aligns y to axis[0] and x to axis[1]
#     LFPy_util.rotation.alignCellToAxes(cell,axes[0],axes[1])

#     sh.push(sim_single_spike,False)
#     # sh.push(sim_morph,True)
#     sh.push(sim_sphere,False)

#     if simulate:
#         sh.simulate()
#     if plot:
#         sh.plot()

# Start simulation(s)
# if simulate or plot:
#     p_arr = []
#     for cnt, nrn in enumerate(neurons):
#         nrn_full = os.path.join(dir_model,nrn)
#         p = Process(target=run, args=(nrn_full,))
#         p.start()
#         p_arr.append(p)
#         # Wait if the number of simulations reaches the number of cores.
#         if cnt % cores == cores-1:
#             for p in p_arr:
#                 p.join()
#             p_arr = []
#     for p in p_arr:
#         p.join()
