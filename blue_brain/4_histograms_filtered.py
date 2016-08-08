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

dir_input = "width_sim_all"
dir_output = "4_histograms_filtered"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRandFilt()
sim_sphere.process_param['spike_to_measure'] = 2

neuron_names = []
widths_I = []
widths_II = []
amps_II = []
dt = None
soma_widths_II = []

pyram = 'pyramidal'
inter = 'inter'
cnt_pyr = 0
cnt_int = 0
# Specify data gather function.
def gather_data(neuron_name, dir_data, sim):
    """
    Gathers data from the simulations into lists.
    """
    # global cnt_int
    # global cnt_pyr
    # if 'PC' in neuron_name:
    #     cnt_pyr += 1
    #     if cnt_pyr > 20:
    #         return
    # else:
    #     cnt_int += 1
    #     if cnt_int > 20:
    #         return
    global dt

    print neuron_name

    neuron_names.append(neuron_name)

    sim.load(dir_data)
    sim.process_data()
    data = sim.data

    widths_I.append(data['widths_I'])
    widths_II.append(data['widths_II'])
    amps_II.append(data['amps_I'])
    soma_widths_II.append(data['soma_width_II'][0])
    if dt is None:
        dt = data['dt']
    if data['dt'] != dt:
        raise ValueError("Mismatching simulations.")
    dt = data['dt']

# Collect data
LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

width_bins = np.arange(0, 2.5, dt)
ampli_bins = np.linspace(0,300, len(width_bins))
bins = [ampli_bins, width_bins]

# {{{ Compute amp. and width histograms.
amp_width_hist = np.zeros([len(neuron_names), len(ampli_bins)-1, len(width_bins)-1])
for i in xrange(len(widths_I)):
    hist, _, _ = np.histogram2d(amps_II[i], widths_I[i], bins)
    hist = hist/float(hist.sum())
    amp_width_hist[i] = hist

pyr_hist_2d = np.zeros(amp_width_hist[0].shape)
int_hist_2d = np.zeros(amp_width_hist[0].shape)
pyr_hist = np.zeros(len(width_bins)-1)
int_hist = np.zeros(len(width_bins)-1)
pyr_hist_II = np.zeros(len(width_bins)-1)
int_hist_II = np.zeros(len(width_bins)-1)

pyr_widths_I = []
pyr_widths_II = []
int_widths_I = []
int_widths_II = []
for i, name in enumerate(neuron_names):
    if 'PC' in name:
        hist_I, _ = np.histogram(widths_I[i], width_bins)
        pyr_hist += hist_I

        hist_II, _ = np.histogram(widths_II[i], width_bins)
        pyr_hist_II += hist_II

        pyr_hist_2d += amp_width_hist[i]

        pyr_widths_I.append(widths_I[i])
        pyr_widths_II.append(widths_II[i])
    else:
        hist_I, _ = np.histogram(widths_I[i], width_bins)
        int_hist += hist_I

        hist_II, _ = np.histogram(widths_II[i], width_bins)
        int_hist_II += hist_II

        int_hist_2d += amp_width_hist[i]

        int_widths_I.append(widths_I[i])
        int_widths_II.append(widths_II[i])

pyr_hist_2d /= pyr_hist_2d.sum()
int_hist_2d /= int_hist_2d.sum()
pyr_hist /= pyr_hist.sum()
int_hist /= int_hist.sum()
pyr_hist_II /= pyr_hist_II.sum()
int_hist_II /= int_hist_II.sum()

pyr_widths_I = np.fromiter(chain.from_iterable(pyr_widths_I), np.float)
pyr_widths_II = np.fromiter(chain.from_iterable(pyr_widths_II), np.float)
int_widths_I = np.fromiter(chain.from_iterable(int_widths_I), np.float)
int_widths_II = np.fromiter(chain.from_iterable(int_widths_II), np.float)

# }}} 

lplot.set_rc_param(True)
lplot.plot_format = ['pdf', 'png']

def overlap(hist_x, hist_y):
    union = np.minimum(hist_x, hist_y)
    intersect = np.maximum(hist_x, hist_y)
    return sum(union)/float(sum(intersect))

def get_roc(negative, positive, thresholds):
    # Inputs all samples unbinned. 
    bins = len(thresholds)
    true_area = float(len(positive))
    false_area = float(len(negative))
    tp = np.zeros(bins)
    fp = np.zeros(bins)
    for k in xrange(bins):
        thresh = thresholds[k]
        tp[k] = (positive <= thresh).sum() / true_area
        fp[k] = (negative <= thresh).sum() / false_area
    return fp, tp

# {{{ ROC curves
fig = plt.figure(figsize=lplot.size_square)

plt.axis('equal')

c = lcmaps.get_short_color_array(3)

y, x = get_roc(int_widths_I, pyr_widths_I, width_bins)
plt.plot(x, y, label='Peak-to-peak Width', color=c[0])

y, x = get_roc(int_widths_II, pyr_widths_II, width_bins)
plt.plot(x, y, label='Half-amp. Width', color=c[1])

ax = plt.gca()
lplot.nice_axes(ax)
ax.set_xlabel(r"True positive rate")
ax.set_ylabel(r"False positive rate")

ticks = np.linspace(0,1,5)
ax.set_xticks(ticks)
ax.set_yticks(ticks)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles,
          labels,
          loc='lower right',
          )

lplot.save_plt(plt, "roc_curves", dir_output)
plt.close()
# }}} 

# {{{ Plot interneuron and pyramidal neuron histograms.
fig, ax = plt.subplots(2,1, 
        sharex=True,
        sharey=True, 
        figsize=lplot.size_common)
dx = (width_bins[1]-width_bins[0])/2.0

c = lcmaps.get_short_color_array(3)

ax[0].bar(width_bins[:-1], int_hist, width=dx, 
        label='Inter.', 
        color=c[1], 
        )
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)

ax[0].bar(width_bins[:-1] + dx, pyr_hist, width=dx, 
        label='Pyramidal',
        color=c[0], 
        )
ax[0].spines['top'].set_visible(False)
ax[0].spines['right'].set_visible(False)

ax[1].bar(width_bins[:-1], int_hist_II, width=dx,
        color=c[1], 
        )
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)

ax[1].bar(width_bins[:-1] + dx, pyr_hist_II, width=dx,
        color=c[0], 
        )
ax[1].spines['top'].set_visible(False)
ax[1].spines['right'].set_visible(False)

handles, labels = ax[0].get_legend_handles_labels()
ax[0].legend(handles,
          labels,
          loc='upper right',
          )

ax[0].set_ylabel(r"Probability")
ax[1].set_ylabel(r"Probability")
ax[1].set_xlabel(r"Width \textbf{[\si{\milli\second}]}")

ax[0].set_title('Peak-to-peak Width')
ax[1].set_title('Half-Amplitude Width')

lplot.save_plt(plt, "int_pyr_width_I_II", dir_output)
plt.close()
# }}} 

# {{{ Plot interneuron and pyramidal neuron histograms 2d 

fig = plt.figure(figsize=lplot.size_common)
gs = mpl.gridspec.GridSpec(1, 2)
ax1 = plt.subplot(gs[0])
ax2 = plt.subplot(gs[1])

# vmax = max(int_hist_2d.max(), pyr_hist_2d.max(), total_hist.max())
vmax = max(int_hist_2d.max(), pyr_hist_2d.max())

aspect = width_bins.max()/ampli_bins.max()

im = ax1.imshow(int_hist_2d, 
        interpolation="none", 
        origin='lower',
        vmin=0,
        vmax=vmax,
        extent=[
            width_bins.min(), 
            width_bins.max(), 
            ampli_bins.min(), 
            ampli_bins.max()])

im = ax2.imshow(pyr_hist_2d, 
        interpolation="none", 
        origin='lower',
        vmin=0,
        vmax=vmax,
        extent=[
            width_bins.min(), 
            width_bins.max(), 
            ampli_bins.min(), 
            ampli_bins.max()])

ax1.set_aspect(aspect)
ax2.set_aspect(aspect)

ticks = np.arange(0, width_bins.max(), 0.5)
ax1.set_xticks(ticks)
ax2.set_xticks(ticks)

ax1.set_xlabel(r"Width \textbf{[\si{\milli\second}]}")
ax2.set_xlabel(r"Width \textbf{[\si{\milli\second}]}")
ax1.set_ylabel(r"Amplitude \textbf{[\si{\micro\volt}]}")

ax1.set_title('Interneurons')
ax2.set_title('Pyramidal Neurons')

cax, kw = mpl.colorbar.make_axes([ax1, ax2])
plt.colorbar(im, cax=cax, **kw)

lplot.save_plt(plt, "int_pyr_hist", dir_output)
plt.close()
# }}} 

# {{{ Compute amp. and width histograms.
hist_TTPC1 = np.zeros(amp_width_hist[0].shape)
hist_TTPC2 = np.zeros(amp_width_hist[0].shape)
hist_UTPC = np.zeros(amp_width_hist[0].shape)
hist_STPC = np.zeros(amp_width_hist[0].shape)
for i, name in enumerate(neuron_names):
    if 'TTPC1' in name:
        hist = hist_TTPC1
    elif 'TTPC2' in name:
        hist = hist_TTPC2
    elif 'UTPC' in name:
        hist = hist_UTPC
    elif 'STPC' in name:
        hist = hist_STPC
    else: continue
    hist += amp_width_hist[i]

hist_TTPC1 /= hist_TTPC1.sum()
hist_TTPC2 /= hist_TTPC2.sum()
hist_UTPC /= hist_UTPC.sum()
hist_STPC /= hist_STPC.sum()
# }}} 

# {{{ Plot pyramidal neuron histograms.
fig = plt.figure(figsize=lplot.size_common)
gs1 = mpl.gridspec.GridSpec(2, 4)
# gs1.update(top=0.8, bottom=0.2)
ax1 = plt.subplot(gs1[0,0])
ax2 = plt.subplot(gs1[0,1])
ax3 = plt.subplot(gs1[1,0])
ax4 = plt.subplot(gs1[1,1])
ax = [ax1, ax2, ax3, ax4]
gs2 = mpl.gridspec.GridSpec(2, 4)
gs2.update(left=0.25)
gs2.update(top=0.75, bottom=0.25)
ax5 = plt.subplot(gs2[:,2:])

ax1.set_xticklabels([])
ax2.set_xticklabels([])
ax2.set_yticklabels([])
ax4.set_yticklabels([])

ax1.set_title('TTPC1')
ax2.set_title('TTPC2')
ax3.set_title('UTPC')
ax4.set_title('STPC')

vmax = max(
        hist_TTPC1.max(),
        hist_TTPC2.max(),
        hist_STPC.max(),
        hist_UTPC.max())

for i, hist in enumerate([hist_TTPC1, hist_TTPC2, hist_UTPC, hist_STPC]):
    im = ax[i].imshow(hist, 
            interpolation="none", 
            origin='lower',
            vmin=0,
            vmax=vmax,
            extent=[
                width_bins.min(), 
                width_bins.max(), 
                ampli_bins.min(), 
                ampli_bins.max()],
            )
    ax[i].set_aspect('auto');

ticks = np.arange(0, width_bins.max(), 0.5)
ax1.set_xticks(ticks)
ax2.set_xticks(ticks)
ax3.set_xticks(ticks)
ax4.set_xticks(ticks)

ax3.set_xlabel(r"Width \textbf{[\si{\milli\second}]}")
ax4.set_xlabel(r"Width \textbf{[\si{\milli\second}]}")
ax1.set_ylabel(r"Amplitude \textbf{[\si{\micro\volt}]}")
ax3.set_ylabel(r"Amplitude \textbf{[\si{\micro\volt}]}")

histograms = [hist_TTPC1, hist_TTPC2, hist_UTPC, hist_STPC]
overlap_mat = np.zeros([len(histograms), len(histograms)])
for i, hist_a in enumerate(histograms):
    for j, hist_b in enumerate(histograms):
        overlap_mat[i,j] = overlap(hist_a.flatten(), hist_b.flatten())

# plt.figure()
im = ax5.imshow(overlap_mat)
plt.colorbar(im, ax=ax5)
plt.xticks(np.arange(4), ('TTPC1', 'TTPC2', 'UTPC', 'STPC'))
plt.yticks(np.arange(4), ('TTPC1', 'TTPC2', 'UTPC', 'STPC'))

lplot.save_plt(plt, "pyr_overlap", dir_output)
plt.close()

# }}} 

# {{{ Save some data to text file.
info = open(dir_output+'/data.txt', 'w')
y, x = get_roc(int_widths_I, pyr_widths_I, width_bins)
score_I = metrics.auc(x, y)
y, x = get_roc(int_widths_II, pyr_widths_II, width_bins)
score_II = metrics.auc(x, y)

soma_width_mean = np.mean(soma_widths_II)
soma_width_std = np.sqrt(np.var(soma_widths_II))

info.write('mean soma width II = {}\n'.format(soma_width_mean))
info.write('std soma width II = {}\n'.format(soma_width_std))
info.write('roc_auc_width_I = {}\n'.format(score_I))
info.write('roc_auc_width_II = {}\n'.format(score_II))
info.write('overlap_width = {}\n'.format(overlap(int_hist, pyr_hist)))
info.write('overlap_width_amp = {}\n'.format(
    overlap(
        int_hist_2d.flatten(), 
        pyr_hist_2d.flatten()
        )))
info.close()
# }}} 
