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
import sklearn.metrics as metrics

dir_input = "width_sim"
dir_output = "width_col"

# Gather directory paths.
dir_current = os.path.dirname(os.path.realpath(__file__))
dir_input = os.path.join(dir_current, dir_input)
dir_output = os.path.join(dir_current, dir_output)

# Specify which simulation to gather data from.
sim_sphere = LFPy_util.sims.SphereRand()
sim_sphere.process_param['spike_to_measure'] = 2
sim_sphere.process_param['assert_width'] = True
# sim_sphere.process_param['width_half_thresh'] = 0.2

neuron_names = []
widths_I = []
widths_II = []
amps_II = []
dt = None

# Specify data gather function.
def gather_data(neuron_name, dir_data, sim):
    """
    Gathers data from the simulations into lists.
    """
    global dt

    # if not "PC" in neuron_name:
    #     return

    print neuron_name
    neuron_names.append(neuron_name)

    sim.load(dir_data)
    sim.process_data()
    data = sim.data

    widths_I.append(data['widths_I'])
    widths_II.append(data['widths_II'])
    amps_II.append(data['amps_I'])
    if dt is None:
        dt = data['dt']
    if data['dt'] != dt:
        raise ValueError("Mismatching simulations.")
    dt = data['dt']

LFPy_util.other.collect_data(dir_input, sim_sphere, gather_data)

sort_indices = np.argsort(neuron_names[:])
neuron_names = np.take(neuron_names, sort_indices)
widths_I = np.take(widths_I, sort_indices)
widths_II = np.take(widths_II, sort_indices)
amps_II = np.take(amps_II, sort_indices)

def jac_score(hist_x, hist_y):
    union = np.minimum(hist_x, hist_y)
    intersect = np.maximum(hist_x, hist_y)
    return sum(union)/float(sum(intersect))

lplot.set_rc_param(False)
lplot.plot_format = ['png']

def get_roc(negative, positive, thresholds):
    bins = len(thresholds)
    true_area = float(len(positive))
    false_area = float(len(negative))
    tp = np.zeros(bins)
    fp = np.zeros(bins)
    # ROC curves
    for k in xrange(bins):
        thresh = thresholds[k]
        tp[k] = (positive <= thresh).sum() / true_area
        fp[k] = (negative <= thresh).sum() / false_area
    return fp, tp

# {{{ amp width roc I meaned
bins = 20
thresholds = np.linspace(0, 2.5, bins)
score = np.zeros([len(neuron_names)/5, len(neuron_names)/5])
meaned = [np.array([]) for _ in range(len(neuron_names)/5)]
for i, nrn in enumerate(neuron_names):
    meaned[i/5] = np.append(meaned[i/5], widths_I[i])
for i in xrange(len(neuron_names)/5):
    for j in xrange(len(neuron_names)/5):
        w1 = meaned[i]
        w2 = meaned[j]
        fp, tp = get_roc(w1, w2, thresholds)
        score[i,j] = metrics.auc(fp, tp)
        if score[i,j] < 0.5:
            score[i,j] = 1 - score[i,j]

plt.imshow(score, interpolation="nearest")
plt.colorbar()
plt.clim(0.5,1.0)
lplot.save_plt(plt, "roc_width_I_meaned", dir_output)
plt.close()
# }}} 

# Roc
bins = 20
positive = widths_I[0]
negative = widths_I[1]
thresholds = np.linspace(0, 2.5, bins)
fp, tp = get_roc(negative, positive, thresholds)
plt.plot(fp, tp, '-ro')
lplot.save_plt(plt, "roc", dir_output)
plt.close()
print metrics.auc(fp, tp)

# {{{ amp width roc
bins = 20
thresholds = np.linspace(0, 2.5, bins)
score = np.zeros([len(neuron_names), len(neuron_names)])
for i, nrn_1 in enumerate(neuron_names):
    for j, nrn_2 in enumerate(neuron_names):
        w1 = widths_I[i]
        w2 = widths_I[j]
        fp, tp = get_roc(w1, w2, thresholds)
        score[i,j] = metrics.auc(fp, tp)
        if score[i,j] < 0.5:
            score[i,j] = 1 - score[i,j]

plt.imshow(score, interpolation="nearest")
plt.colorbar()
plt.clim(0.5,1.0)
lplot.save_plt(plt, "roc_width", dir_output)
plt.close()
# }}} 

# {{{ 
widths_I_hist = []
# bin_edges = np.arange(0, 2.5, dt)
bin_edges = np.linspace(0, 2.5, 20)
for i in xrange(len(widths_I)):
    hist, _ = np.histogram(widths_I[i], bin_edges)
    hist = hist/float(sum(hist))
    hist = np.round(hist*1000)
    widths_I_hist.append(hist)
jaccard_index = np.zeros([len(neuron_names), len(neuron_names)])
for i, nrn_1 in enumerate(neuron_names):
    for j, nrn_2 in enumerate(neuron_names):
        jaccard_index[i,j] = jac_score(widths_I_hist[i], widths_I_hist[j])
plt.imshow(jaccard_index, interpolation="nearest")
plt.colorbar()
plt.clim(0,1.0)
lplot.save_plt(plt, "hist_width_I", dir_output)
plt.close()
# }}} 

# {{{ 
widths_II_hist = []
# bin_edges = np.arange(0, 2.5, dt)
bin_edges = np.linspace(0, 2.5, 20)
for i in xrange(len(widths_II)):
    hist, _ = np.histogram(widths_II[i], bin_edges)
    hist = hist/float(sum(hist))
    hist = np.round(hist*1000)
    widths_II_hist.append(hist)
jaccard_index = np.zeros([len(neuron_names), len(neuron_names)])
for i, nrn_1 in enumerate(neuron_names):
    for j, nrn_2 in enumerate(neuron_names):
        jaccard_index[i,j] = jac_score(widths_II_hist[i], widths_II_hist[j])
plt.imshow(jaccard_index, interpolation="nearest")
plt.colorbar()
plt.clim(0,1.0)
lplot.save_plt(plt, "hist_width_II", dir_output)
plt.close()
# }}} 

# {{{ amp width hist
amp_width_hist = []
# width_bin_edges = np.arange(0, 2.5, dt)
width_bin_edges = np.linspace(0, 2.5, 20)
amp_bin_edges = np.linspace(0,300,20)
bin_edges = [amp_bin_edges, width_bin_edges]
for i in xrange(len(widths_I)):
    hist, _, _ = np.histogram2d(amps_II[i], widths_I[i], bin_edges)
    hist = hist/float(hist.sum())
    hist = np.round(hist*1000)
    amp_width_hist.append(hist)
jaccard_index = np.zeros([len(neuron_names), len(neuron_names)])
for i, nrn_1 in enumerate(neuron_names):
    for j, nrn_2 in enumerate(neuron_names):
        jaccard_index[i,j] = jac_score(
                amp_width_hist[i].flatten(), 
                amp_width_hist[j].flatten(),
                )
plt.imshow(jaccard_index, interpolation="nearest")
plt.colorbar()
plt.clim(0,1.0)
lplot.save_plt(plt, "hist_amp_width", dir_output)

plt.imshow(jaccard_index>0.3, interpolation="nearest")
lplot.save_plt(plt, "hist_amp_width_thresh", dir_output)

plt.close()
# }}} 

print "hist"
for i, name in enumerate(neuron_names):
    print name
    plt.imshow(amp_width_hist[i], interpolation="nearest")
    plt.colorbar()
    lplot.save_plt(plt, name+"_hist", dir_output)
    plt.close()




