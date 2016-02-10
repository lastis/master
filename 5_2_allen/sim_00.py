"""
Attempt at using models from allen.
"""
import os
import LFPy_util
import allen
# pylint: disable=invalid-name

allen.download_all_models()
model_index = [1]
# model_index = range(2,len(allen.MODEL_NUMS))
model_names = [str(model_id) for i, model_id in enumerate(allen.MODEL_NUMS) if i in model_index]

# Compile and load the extra mod file(s). The ISyn electrode.
dir_mod = os.path.join(allen.DIR_RES, 'extra_mod/')
LFPy_util.other.nrnivmodl(dir_mod)

def load_cell(neuron_name):
    """
    Loads a cell object from allen.
    """
    # start_ms = 0.
    # stop_ms = 1400.
    cell = allen.load_cell_by_id(int(neuron_name))
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    cell.tstartms = 0
    cell.tstopms = 1400
    return cell

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_cell)
sim.set_dir_neurons("sim_00")
sim.set_neuron_name(model_names)
sim.simulate = True
sim.plot = True
sim.parallel_plot = True

### Simulation objects.
sim_multi = LFPy_util.sims.MultiSpike()
sim_multi.run_param['pptype'] = 'ISyn'
sim_multi.run_param['threshold'] = 4
sim_multi.run_param['delay'] = 200
sim_multi.run_param['duration'] = 1000
sim_multi.run_param['pre_dur'] = 16.7*0.2
sim_multi.run_param['post_dur'] = 16.7*0.8
sim_multi.run_param['spikes'] = 3
sim_multi.verbose = True

sim_intra = LFPy_util.sims.Intracellular()

sim_sphere = LFPy_util.sims.SphereElectrodes()
sim_sphere.elec_to_plot = range(10)
sim_sphere.process_param['spike_to_measure'] = 1

sim_sym = LFPy_util.sims.SymmetryFiltered()
sim_sym.process_param['spike_to_measure'] = 1

sim_morph = LFPy_util.sims.Morphology()

sim_grid = LFPy_util.sims.Grid()
sim_grid_dense = LFPy_util.sims.GridDense()
###

sim.push(sim_multi, False)
# sim.push(sim_intra, True)
# sim.push(sim_sphere, True)
sim.push(sim_sym, True)
# sim.push(sim_morph, True)
# sim.push(sim_grid, True)
# sim.push(sim_grid_dense, True)

print sim
sim.run()
