"""
Attempt at using models from allen.
"""
import os
import LFPy_util
import allen
# pylint: disable=invalid-name

allen.download_all_models()
# model_index = [1,2,3,4]
model_index = range(2,len(allen.MODEL_NUMS))
model_names = [str(model_id) for i, model_id in enumerate(allen.MODEL_NUMS) if i in model_index]

# Compile and load the extra mod file(s). The ISyn electrode.
dir_mod = os.path.join(allen.DIR_RES, 'extra_mod/')
LFPy_util.other.nrnivmodl(dir_mod)

def load_cell(neuron_name):
    """
    Loads a cell object from allen.
    """
    start_ms = -150.
    stop_ms = 300.
    cell = allen.load_cell_by_id(int(neuron_name),start_ms,stop_ms)
    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.find_major_axes()
    # Aligns y to axis[0] and x to axis[1]
    LFPy_util.rotation.alignCellToAxes(cell, axes[0], axes[1])
    return cell

sim = LFPy_util.Simulator()
sim.set_cell_load_func(load_cell)
sim.set_dir_neurons("sim_00")
sim.set_neuron_name(model_names)
sim.simulate = True
sim.plot = True

# Simulation objects.
sim_single_spike = LFPy_util.sims.SingleSpike()
sim_single_spike.run_param['pptype'] = 'ISyn'
sim_single_spike.run_param['threshold'] = 4
sim_single_spike.debug = True
sim_intra = LFPy_util.sims.Intracellular()
sim_sphere = LFPy_util.sims.SphereElectrodes()
sim_sphere.elec_to_plot = range(10)
sim_sym = LFPy_util.sims.Symmetry()
sim_morph = LFPy_util.sims.Morphology()

sim.push(sim_single_spike, False)
sim.push(sim_intra, True)
sim.push(sim_sphere, True)
sim.push(sim_sym, True)
sim.push(sim_morph, True)

print sim
sim.run()
