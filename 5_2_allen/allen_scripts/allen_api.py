import os
from allensdk.api.queries.biophysical_perisomatic_api import \
    BiophysicalPerisomaticApi
from allensdk.api.queries.cell_types_api import CellTypesApi

# http://api.brain-map.org/api/v2/data/query.xml?criteria=
# model::Specimen
# ,rma::criteria,neuronal_models(neuronal_model_template[name$eq'Biophysical - perisomatic'])


model_dir = 'res/allen_models'
if not os.path.exists(model_dir):
    os.makedirs(model_dir)

# bp = BiophysicalPerisomaticApi('http://api.brain-map.org')
# # change to False to not download the large stimulus NWB file
# bp.cache_stimulus = False 
# # get this from the web site as above
# neuronal_model_id = 472451419    
# bp.cache_data(neuronal_model_id, working_directory=model_dir)
os.chdir(model_dir)
import LFPy_util
import LFPy
from glob import glob
morphologyfile = glob("*.swc")[0]
print morphologyfile

import allensdk.model.biophysical_perisomatic as bp
import allensdk.model.biophysical_perisomatic.runner as runner
# config = runner.load_description(os.path.join(model_dir,"manifest.json"))
config = runner.load_description("manifest.json")
utils = bp.utils.Utils(config)
# morphology_path = config.manifest.get_path('MORPHOLOGY')
# utils.generate_morphology(morphology_path.encode('ascii', 'ignore'))
cell = LFPy.Cell(
    morphology=morphologyfile,
    tstartms=0,
    tstopms=300.,
    pt3d=True,
    timeres_NEURON=2** -5,
    timeres_python=2** -5, )
utils.load_cell_parameters()


# import allensdk.model.biophysical_perisomatic as bp
# config = bp.runner.load_description(os.path.join(model_dir,"manifest.json"))
# util = bp.utils.Utils(config)


# LFPy_util.other.nrnivmodl(os.path.join(model_dir,'modfiles'))
# Instantiate the cell(s) using LFPy

sim = LFPy_util.Simulator()
sim.set_cell(cell)
sim.set_dir_neurons("neurons")
sim.set_neuron_name("test_neuron")
sim.simulate = True
sim.plot = True

# Simulation objects.
sim_single_spike = LFPy_util.sims.SingleSpike()
sim_single_spike.debug = True
# sim_single_spike.run_param['init_amp'] = -1
sim_intra = LFPy_util.sims.Intracellular()
sim_sphere = LFPy_util.sims.SphereElectrodes()
sim_sphere.elec_to_plot = range(10)
sim_sym = LFPy_util.sims.Symmetry()
sim_morph = LFPy_util.sims.Morphology()

sim.push(sim_single_spike, False)
sim.push(sim_intra, True)
# sim.push(sim_sphere, True)
# sim.push(sim_sym, True)
# sim.push(sim_morph, True)

print sim
sim.run()

# ct = CellTypesApi()

# # a list of dictionaries containing metadata for cells with reconstructions
# cells = ct.list_cells(require_reconstruction=True)

# # download the electrophysiology data for one cell
# ct.save_ephys_data(cells[0]['id'], 'example.nwb')

# # download the reconstruction for the same cell
# ct.save_reconstruction(cells[0]['id'], 'example.swc')
