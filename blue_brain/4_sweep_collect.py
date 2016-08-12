"""
Compare width analysis for TTPC and NBC, LBC.
"""
# pylint: disable=invalid-name
import os
import numpy as np
import LFPy_util
import LFPy_util.plot as lplot
import LFPy_util.colormaps as lcmaps
import LFPy_util.data_extraction as de
import matplotlib.pyplot as plt
import matplotlib as mpl
import sklearn.metrics as metrics
from itertools import chain

dir_data = "4_sweep_sim/L5_TTPC1_cADpyr232_1/data"
dir_output = "4_sweep_collect"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_data = os.path.join(dir_current, dir_data)
dir_output = os.path.join(dir_current, dir_output)

sim = LFPy_util.sims.CurrentSweep()
sim.load(dir_data)
sim.process_data()

lplot.set_rc_param(True)
lplot.plot_format = ['pdf', 'png']

elec_to_plot = 0

# {{{ plot freq_amp_soma_elec
plt.figure(figsize=lplot.size_common)
fig = plt.figure(figsize=lplot.size_common)
gs = mpl.gridspec.GridSpec(1, 2)
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot(sim.data['freqs'],
         sim.data['amps_I_soma_mean'],
         color=lcmaps.get_color(0),
         marker='o',
         markersize=5,
         label='Soma',
         )
ax1.fill_between(sim.data['freqs'],
                sim.data['amps_I_soma_mean'] - sim.data['amps_I_soma_std'],
                sim.data['amps_I_soma_mean'] + sim.data['amps_I_soma_std'],
                color=lcmaps.get_color(0),
                alpha=0.2)
ax2.plot(sim.data['freqs'],
         sim.data['amps_I_elec_mean'][:, elec_to_plot],
         color=lcmaps.get_color(0.5),
         marker='o',
         markersize=5,
         label='Elec.'
         )
ax2.fill_between(
        sim.data['freqs'],
        sim.data['amps_I_elec_mean'][:,elec_to_plot] 
            - sim.data['amps_I_elec_std'][:,elec_to_plot],
        sim.data['amps_I_elec_mean'][:,elec_to_plot] 
            + sim.data['amps_I_elec_std'][:,elec_to_plot],
        color=lcmaps.get_color(0.5),
        alpha=0.2)
ax1.set_ylabel(r"Base-to-Peak Amp. \textbf{[\si{\milli\volt}]}")
ax2.set_ylabel(r"Base-to-Peak Amp. \textbf{[\si{\micro\volt}]}")
ax1.set_xlabel(r"Frequency \textbf{[\si{\hertz}]}")
ax2.set_xlabel(r"Frequency \textbf{[\si{\hertz}]}")

ax1.set_title('Soma')
ax2.set_title('Electrode')

lplot.save_plt(plt, "freq_amp_soma_elec", dir_output)
plt.close()
# }}} 

# {{{ plot freq_width_soma_elec
plt.figure(figsize=lplot.size_common)
fig = plt.figure(figsize=lplot.size_common)
gs = mpl.gridspec.GridSpec(1, 2, wspace=0.3)
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

ax1.plot(sim.data['freqs'],
         sim.data['widths_II_soma_mean'],
         color=lcmaps.get_color(0),
         marker='o',
         markersize=5,
         label='Soma',
         )
ax1.fill_between(sim.data['freqs'],
                sim.data['widths_II_soma_mean'] - sim.data['widths_II_soma_std'],
                sim.data['widths_II_soma_mean'] + sim.data['widths_II_soma_std'],
                color=lcmaps.get_color(0),
                alpha=0.2)
ax2.plot(sim.data['freqs'],
         sim.data['widths_II_elec_mean'][:, elec_to_plot],
         color=lcmaps.get_color(0.5),
         marker='o',
         markersize=5,
         label='Elec.'
         )
ax2.fill_between(
        sim.data['freqs'],
        sim.data['widths_II_elec_mean'][:,elec_to_plot] 
            - sim.data['widths_II_elec_std'][:,elec_to_plot],
        sim.data['widths_II_elec_mean'][:,elec_to_plot] 
            + sim.data['widths_II_elec_std'][:,elec_to_plot],
        color=lcmaps.get_color(0.5),
        alpha=0.2)
ax1.set_ylabel(r"Half-amp. Width \textbf{[\si{\milli\second}]}")
ax2.set_ylabel(r"Half-amp. Width \textbf{[\si{\milli\second}]}")
ax1.set_xlabel(r"Frequency \textbf{[\si{\hertz}]}")
ax2.set_xlabel(r"Frequency \textbf{[\si{\hertz}]}")

ax1.set_title('Soma')
ax2.set_title('Electrode')

ticks = np.arange(0, sim.data['freqs'].max()+1, 5)
ax1.set_xticks(ticks)
ax2.set_xticks(ticks)

# Increase the gap between plots to make room for axis label. 

lplot.save_plt(plt, "freq_width_soma_elec", dir_output)
plt.close()
# }}} 
