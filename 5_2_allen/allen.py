"""
Helps download and load biophysical biophysical perisomatic models from
allen brain institute.
"""
import os
from glob import glob
import LFPy_util
import LFPy
import allensdk.model.biophysical_perisomatic as bp
import allensdk.model.biophysical_perisomatic.runner as runner
from allensdk.api.queries.biophysical_perisomatic_api \
    import BiophysicalPerisomaticApi
MODEL_NUMS = [
    472424854,
    473871773,
    473561660,
    472306460,
    471087975,
    472450023,
    472455509,
    473835796,
    472299363,
    473862421,
    473465774,
    472447460,
    472912177,
    473561729,
    472349114,
    471085845,
]
DIR_PROJECT = os.path.dirname(os.path.realpath(__file__))
DIR_RES = os.path.join(DIR_PROJECT, 'res/')
DIR_MODELS = os.path.join(DIR_PROJECT, 'res/allen_models')


def download_all_models():
    """
    Import models specified in the module constant.
    """
    # If folder doesn't exist, download the models.
    if not os.path.exists(DIR_MODELS):
        os.makedirs(DIR_MODELS)

        # Download models.
        bpa = BiophysicalPerisomaticApi('http://api.brain-map.org')
        # change to False to not download the large stimulus NWB file
        bpa.cache_stimulus = False
        # get this from the web site as above
        for mod_id in MODEL_NUMS:
            new_dir = os.path.join(DIR_MODELS, str(mod_id))
            bpa.cache_data(mod_id, working_directory=new_dir)


def get_model_dir_by_id(model_id):
    """
    Get the path to the directory using the id of the model in
    allen.MODEL_NUMS.
    """
    index = MODEL_NUMS.index(model_id)
    return get_model_dir(index)


def get_model_dir(index):
    """
    Get the path to the directory using the index of the model in
    allen.MODEL_NUMS.
    """
    return os.path.join(DIR_MODELS, str(MODEL_NUMS[index]))


def load_cell_by_id(model_id, start_ms=0., stop_ms=300.):
    """
    Load a cell object using the id of the model in allen.MODEL_NUMS.
    """
    dir_model = get_model_dir_by_id(model_id)
    dir_modfiles = os.path.join(dir_model, 'modfiles')
    # path_manifest = os.path.join(dir_model, "manifest.json")
    path_morp = glob(os.path.join(dir_model, "*.swc"))[0]

    # Compile the mod files.
    LFPy_util.other.nrnivmodl(dir_modfiles, suppress=True)

    cell = LFPy.Cell(
        morphology=path_morp,
        tstartms=start_ms,
        tstopms=stop_ms,
        pt3d=True,
        timeres_NEURON=2 ** -5,
        timeres_python=2 ** -5,
        v_init=-80,
        )

    cwd = os.getcwd()
    os.chdir(dir_model)
    description = runner.load_description('manifest.json')
    utils = bp.utils.Utils(description)
    utils.load_cell_parameters()
    os.chdir(cwd)
    return cell


def load_cell(model_index, start_ms=0., stop_ms=300.):
    """
    Load a cell object using the index of the model in allen.MODEL_NUMS.
    """
    model_id = MODEL_NUMS[model_index]
    return load_cell_by_id(model_id, start_ms, stop_ms)
