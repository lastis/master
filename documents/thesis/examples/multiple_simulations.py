import LFPy_util
from load_model import get_cell
from new_simulation_class import CustomSimulation

sim = LFPy_util.Simulator()
sim.set_cell_load_func(get_cell)
# The string is passed to the get_cell function.
sim.set_neuron_name("pyramidal_1")

sim_custom_1 = CustomSimulation()
sim_custom_1.run_param['amp'] = 1.25 # nA

sim_custom_2 = CustomSimulation()
sim_custom_2.run_param['amp'] = 0.75 # nA
# Avoid sim_custom_2 overwriting the data from sim_custom_1.
sim_custom_2.set_name("custom_sim_2")

# Add the simulations to a list we want to run.
sim.push(sim_custom_1)
sim.push(sim_custom_2)

sim.simulate()
sim.plot()
