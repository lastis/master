import numpy as np

def tetrode_spikes_mean_max(signal, amp_option='pos'):
    """
    Input is a 3d array, (spikes x electrodes x time)
    Takes the strongest signal from each electrode and means them.

    Each electrode records the same spike.
    """
    if amp_option == 'pos':
        pass
    elif amp_option == 'neg':
        signal = -signal
    elif amp_option == 'both':
        signal = np.fabs(signal)
    # Take the maximum of all signals
    signal_max = np.amax(signal, axis=2)
    # Make a list with the index of the electrode that has the highest value
    # for each spike.
    signal_max_idx = np.argmax(signal_max, axis=1)
    cols = signal.shape[0]
    signal_out = np.mean(signal[np.arange(cols),signal_max_idx], axis=0)
    signal_out_std = np.sqrt(np.var(signal[np.arange(cols), signal_max_idx], axis=0))
    return signal_out, signal_out_std


