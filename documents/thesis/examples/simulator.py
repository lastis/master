import LFPy_util
from load_model import get_cell

def get_simulator(neuron_name):
    sim = LFPy_util.Simulator()
    sim.set_cell_load_func(get_cell)
    sim.set_output_dir("multiple_neurons")
    sim.set_neuron_name(neuron_name)

    sim_electrode = LFPy_util.sims.MultiSpike()
    sim_electrode.run_param['spikes'] = 3

    sim_intra = LFPy_util.sims.Intracellular()

    sim.push(sim_electrode, False)
    sim.push(sim_intra)
    
    return sim
