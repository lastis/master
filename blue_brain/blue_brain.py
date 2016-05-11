"""
Helper functions for loading models from BlueBrain.
"""
import os
import urllib
import tarfile
import zipfile
import shutil
from glob import glob
import subprocess
import neuron
import LFPy
import LFPy_util

# Gather directory paths.
# Find the location of 5_1_blue_brain folder.
DIR_PROJECT = os.path.dirname(os.path.realpath(__file__))
DIR_RES = os.path.join(DIR_PROJECT, 'res/')
DIR_MODELS = os.path.join(DIR_PROJECT, 'res/bbp_models')


def load_model(nrn, add_synapses=False, comp=True, suppress=False):
    """
    Load a model from the bluebrain model folder. Returns a list of cells.
    """
    # pylint: disable=too-many-locals
    # Load some dependencies.
    neuron.h.load_file('stdrun.hoc')
    neuron.h.load_file('import3d.hoc')

    # Suppress neuron output.
    if suppress:
        # Open a pair of null files
        null_fds = [os.open(os.devnull, os.O_RDWR) for _ in range(2)]
        # Save the actual stdout (1) and stderr (2) file descriptors.
        save_fds = (os.dup(1), os.dup(2))
        os.dup2(null_fds[0], 1)
        os.dup2(null_fds[1], 2)

    # Load mod files of the neuron.
    mechanism_mod_dir = os.path.join(nrn, 'mechanisms')
    LFPy_util.other.nrnivmodl(mechanism_mod_dir, suppress)

    os.chdir(nrn)
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

    if not hasattr(neuron.h, morphology):
        # Load morphology
        neuron.h.load_file(1, "morphology.hoc")
    if not hasattr(neuron.h, biophysics):
        # Load biophysics
        neuron.h.load_file(1, "biophysics.hoc")
    if not hasattr(neuron.h, synapses):
        # load synapses
        neuron.h.load_file(1, os.path.join('synapses', 'synapses.hoc'))
    if not hasattr(neuron.h, templatename):
        # Load main cell template
        neuron.h.load_file(1, "template.hoc")

    cells = []
    # One cell model can have multiple morphologies.
    for morphologyfile in glob('morphology/*'):
        # Instantiate the cell(s) using LFPy
        cell = LFPy.TemplateCell(
            morphology=morphologyfile,
            templatefile=os.path.join(nrn, 'template.hoc'),
            templatename=templatename,
            templateargs=1 if add_synapses else 0,
            tstartms=0,
            tstopms=300.,
            pt3d=True,
            timeres_NEURON=2 ** -5,
            timeres_python=2 ** -5, 
            passive=False,
            v_init=-70,
            )
        cells.append(cell)

    if suppress:
        # Re-assign the real stdout/stderr back to (1) and (2)
        os.dup2(save_fds[0], 1)
        os.dup2(save_fds[1], 2)
        # Close the null files
        os.close(null_fds[0])
        os.close(null_fds[1])
    return cells


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
            # print 'template {} found!'.format(templatename)
            continue

    return templatename


def download_all_models(model_dir='bbp_models'):
    """
    Download models from bluebrain if missing.
    """
    # Download the cell models if they do not exist.
    if not os.path.isdir(model_dir):
        print 'Model files not found. '
        print 'Downloading all bbp models. About 785 mb, can take time.'
        file_url = "https://bbp.epfl.ch/nmc-portal/documents/10184/" \
                   "7288948/hoc_combos_syn.1_0_10.allzips.tar/" \
                   "cef96ba5-35ea-45a9-a2ef-2f27ec12ae6b"
        tar_path = os.path.join(model_dir, 'all_models.tar')
        untarred_folder = os.path.join(model_dir,
                                       'hoc_combos_syn.1_0_10.allzips')

        os.makedirs(model_dir)

        opener = urllib.URLopener()
        print 'Downloading: {}'.format(tar_path)
        # Temporary store the tar file.
        opener.retrieve(file_url, tar_path)

        # Untar.
        print 'Untaring   : {}'.format(tar_path)
        print 'Untaring to: {}'.format(untarred_folder)
        t_file = tarfile.open(tar_path)
        # Extract all contents in the tar file.
        t_file.extractall(model_dir)

        # Delete the big tar file.
        print 'Removing   : {}'.format(tar_path)
        os.remove(tar_path)

        # Unzip all the files.
        print 'Unzipping  : {}/*.zip'.format(untarred_folder)
        os.chdir(untarred_folder)
        for zip_file_name in glob('*.zip'):
            zip_file = zipfile.ZipFile(zip_file_name)
            # Exract the file to the model dir.
            zip_file.extractall(model_dir)
        print 'Removing   : {}'.format(untarred_folder)
        shutil.rmtree(untarred_folder)
