from simulator import get_simulator

neurons = ["pyramidal_1", "pyramidal_2"]

simm = LFPy_util.SimulatorManager()
# Number of LFPy_util.Simulator objects  that will run in parallel.
simm.concurrent_neurons = 8
simm.set_neuron_names(neurons)
simm.set_sim_load_func(get_simulator)

simm.simulate()
simm.plot()
