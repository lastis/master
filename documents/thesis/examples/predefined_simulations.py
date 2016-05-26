import LFPy_util
from load_model import get_cell

sim = LFPy_util.Simulator()
sim.set_cell_load_func(get_cell)
sim.set_output_dir("predefined_simulations")

sim.set_neuron_name("pyramidal_1")

sim_electrode = LFPy_util.sims.MultiSpike()
sim_electrode.run_param['spikes'] = 3

sim_intra = LFPy_util.sims.Intracellular()

# Add the simulations to a list we want to run.
sim.push(sim_electrode, False)
sim.push(sim_intra)

sim.simulate()
sim.plot()
