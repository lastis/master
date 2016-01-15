#import some plotting stuff and the LFPy-module
import os
import sys
import LFPy
import LFPy_util.plot
import numpy as np
import neuron
from neuron import h as h

file_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(file_path)

def init():
    cellParameters = {
        'morphology' : os.path.join(project_dir,'res/morphology/example.swc'),
        'rm' : 30000,               # membrane resistance
        'cm' : 1.0,                 # membrane capacitance
        'Ra' : 150,                 # axial resistance
        'v_init' : -65,             # initial crossmembrane potential
        'e_pas' : -65,              # reversal potential passive mechs
        'passive' : True,           # switch on passive mechs
        'lambda_f' : 500,           # segments are isopotential at this frequency
        'timeres_NEURON' : 2**-5,   # dt of LFP and NEURON simulation.
        'timeres_python' : 2**-5,
        'tstartms' : 0,           #start time, recorders start at t=0
        'tstopms' : 16.7,             #stop time of simulation
        'pt3d' : True,
    }


    #Initialize cell instance, using the LFPy.Cell class
    cell = LFPy.Cell(**cellParameters)
    return cell
