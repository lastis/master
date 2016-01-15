import LFPy
import LFPy_util
import LFPy_util.simulations
import LFPy_util.data_extraction
import LFPy_util.plot
import LFPy_util.rotation
import LFPy_util.meshgen
import LFPy_util.electrodes
from neuron import h
import numpy as np
import os.path
import os
from multiprocessing import Process


file_path = os.path.dirname(os.path.realpath(__file__))
project_dir = os.path.dirname(file_path)
plot_dir = os.path.join(project_dir,'results/plot')
param_dir = os.path.join(project_dir, 'res/plot_param')

show = False

# Grid Parameters.
nx = 20
ny = 20
# Circular Parameters.
n_theta = 10
r = 200
n = 11
n_theta = 10
r_0 = 10
dr = (r-r_0)/n
dt = 0.025
threshold = 0.75


def run(cell):
    # Play an action potential.
    path = os.path.join(project_dir,'res/cs_ap.js')
    param = LFPy_util.plot.getDictFromPlotParamFile(path)
    v_vec = np.array(param['v_vec'])
    t_vec = np.array(param['t_vec'])
    dt = param['dt']
    v_vec = h.Vector(v_vec)
    t_vec = h.Vector(t_vec)
    # v_vec.play(h.soma[0](0.5)._ref_v, t_vec)
    for sec in cell.somalist:
        v_vec.play(sec(0.5)._ref_v, t_vec)

    # Find the principal component axes and rotate cell.
    axes = LFPy_util.data_extraction.findMajorAxes()
    LFPy_util.rotation.alignCellToAxes(cell,axes[0],axes[1])

    # Soma.
    LFPy_util.simulations.soma(cell,param_dir)
    # Grid electrodes.
    x = np.linspace(-200,200,nx)
    y = np.linspace(-200,200,ny)
    LFPy_util.simulations.gridXY(cell,x,y,param_dir)
    # Circular electrodes.
    LFPy_util.simulations.circularXZ(cell,n,n_theta,r,r_0,param_dir)

def plot():
    LFPy_util.simulations.soma(
        param_dir   = param_dir,
        plot_dir    = plot_dir,
    )
    LFPy_util.simulations.circularXZ(
        param_dir   = param_dir,
        plot_dir    = plot_dir,
    )
    LFPy_util.simulations.gridXY(
        param_dir   = param_dir,
        plot_dir    = plot_dir,
    )
