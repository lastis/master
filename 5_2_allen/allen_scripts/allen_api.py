from allensdk.api.queries.biophysical_perisomatic_api import \
    BiophysicalPerisomaticApi
from allensdk.api.queries.cell_types_api import CellTypesApi

# bp = BiophysicalPerisomaticApi('http://api.brain-map.org')
# # change to False to not download the large stimulus NWB file
# bp.cache_stimulus = True 
# # get this from the web site as above
# neuronal_model_id = 472451419    
# bp.cache_data(neuronal_model_id, working_directory='neuronal_model')


ct = CellTypesApi()

# a list of dictionaries containing metadata for cells with reconstructions
cells = ct.list_cells(require_reconstruction=True)

# download the electrophysiology data for one cell
ct.save_ephys_data(cells[0]['id'], 'example.nwb')

# download the reconstruction for the same cell
ct.save_reconstruction(cells[0]['id'], 'example.swc')
