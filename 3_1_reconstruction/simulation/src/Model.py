#import some plotting stuff and the LFPy-module
import os
import LFPy
import numpy as np
import matplotlib.pyplot as plt
import neuron
from neuron import h as h
import LFPy_util.plot

file_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(file_path)

def init():
    #define cell parameters used as input to cell-class
    cellParameters = {
        'morphology' : os.path.join(project_dir,'res/morphology/L5_Mainen96_LFPy.hoc'),
        'rm' : 30000,               # membrane resistance
        'cm' : 1.0,                 # membrane capacitance
        'Ra' : 150,                 # axial resistance
        'v_init' : -0,             # initial crossmembrane potential
        'e_pas' : -0,              # reversal potential passive mechs
        'passive' : True,           # switch on passive mechs
        'timeres_NEURON' : 2**-5,   # dt of LFP and NEURON simulation.
        'timeres_python' : 2**-5,
        'tstartms' : -00,           #start time, recorders start at t=0
        'tstopms' : 16.7,             #stop time of simulation
        'pt3d' : True,
    }

    #Initialize cell instance, using the LFPy.Cell class
    cell = LFPy.Cell(**cellParameters)

    # soma_clamp_params = {
    #     'idx': cell.somaidx,
    #     'record_current': True,
    #     'amp': 15, #  [nA]
    #     'dur': 6.,  # [ms]
    #     'delay': 5,  # [ms]
    #     'pptype': 'IClamp',
    # }
    # stim = LFPy.StimIntElectrode(cell, **soma_clamp_params)
    return cell
