import LFPy
import LFPy_util
import os
import numpy as np
import neuron
from glob import glob

# Location of the models.
DIR_FILE = os.path.dirname(os.path.realpath(__file__))
DIR_MODELS = os.path.join(DIR_FILE, 'res/')

def get_cell(neuron_name):
    """
    Load a spesific model based on a string and return a LFPy Cell object.

    :param string neuron_name:
        String to identify the neuron model that will be loaded.
    :return:
        Cell Object from LFPy.
    """
    original_cwd = os.getcwd()

    neuron.h.load_file('stdrun.hoc')
    neuron.h.load_file('import3d.hoc')

    # Use the neuron name to find the desired model.
    dir_nrn_model = os.path.join(DIR_MODELS, neuron_name)

    # Load mod files of the neuron.
    mechanism_mod_dir = os.path.join(dir_nrn_model, 'mechanisms')
    LFPy_util.other.nrnivmodl(mechanism_mod_dir)

    # The following .hoc files are spesific for the blue brain models.
    os.chdir(dir_nrn_model)
    #get the template name
    tmp_file = file("template.hoc", 'r')
    templatename = get_templatename(tmp_file)
    tmp_file.close()
    #get biophys template name
    tmp_file = file("biophysics.hoc", 'r')
    biophysics = get_templatename(tmp_file)
    tmp_file.close()
    #get morphology template name
    tmp_file = file("morphology.hoc", 'r')
    morphology = get_templatename(tmp_file)
    tmp_file.close()
    #get synapses template name
    tmp_file = file(os.path.join("synapses", "synapses.hoc"), 'r')
    synapses = get_templatename(tmp_file)
    tmp_file.close()
    neuron.h.load_file('constants.hoc')

    if not hasattr(neuron.h, templatename):
        # Load main cell template
        neuron.h.load_file(1, "template.hoc")
    if not hasattr(neuron.h, morphology):
        # Load morphology
        neuron.h.load_file(1, "morphology.hoc")
    if not hasattr(neuron.h, biophysics):
        # Load biophysics
        neuron.h.load_file(1, "biophysics.hoc")
    if not hasattr(neuron.h, synapses):
        # load synapses
        neuron.h.load_file(1, os.path.join('synapses', 'synapses.hoc'))


    for morphologyfile in glob('morphology/*'):
        # Instantiate the cell(s) using LFPy
        cell = LFPy.TemplateCell(
            morphology=morphologyfile,
            templatefile=os.path.join(neuron_name, 'template.hoc'),
            templatename=templatename,
            templateargs=0,
            tstartms=0,
            tstopms=300.,
            pt3d=True,
            timeres_NEURON=2 ** -5,
            timeres_python=2 ** -5, 
            passive=False,
            v_init=-70,
            )
        # Reset back to the previous working directory.
        os.chdir(original_cwd)
        return cell


def get_templatename(file_template):
    '''
    Assess from hoc file the templatename being specified within

    Arguments
    ---------
    file_template : file, mode 'r'

    Returns
    -------
    templatename : str

    '''
    file_template = file("template.hoc", 'r')
    for line in file_template.readlines():
        if 'begintemplate' in line.split():
            templatename = line.split()[-1]
            continue

    return templatename
