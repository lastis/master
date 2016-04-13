import numpy as np
import pylab as plt
import LFPy_util.plot
import LFPy_util.data_extraction
from scipy.signal import argrelextrema
import pdb


def set_parameters_sweep(a):
    '''
    Defines simulation, stimulus and neuron parameters and stores values in parameter dictionary p.

    Returns:
    --------
    p : dict
        Parameter dictionary.
      
    '''

    ## initialise new dictionary
    p = {}

    ## simulation parameters
    p['T'] = 500  ## simulation time (ms)
    p['dt'] = 2** -4  ## simulation time resolution (ms)
    p['t_start'] = -100

    ## stimulus parameters
    p['I_amp'] = a  ## input current amplitude (uA/cm2)
    p['t_stim_on'] = -50  ## stimulus-on time (ms)
    p['t_stim_off'] = p['T']  ## stimulus-off time (ms)

    ## neuron parameters
    p['V_rest'] = -68.  ## resting potential (mV)
    p['Cm'] = 1.  ## membrane capacitance (uF/cm2)
    p['gbar_Na'] = 120.  ## max. Na conductance (mS/cm2)
    p['gbar_K'] = 20.  ## max K conductance (mS/cm2)
    p['gbar_l'] = 0.3  ## leak conductance (mS/cm2)
    p['gbar_A'] = 47.7
    p['E_Na'] = 55.  ## Na reversal potentail (mV)
    p['E_K'] = -72.  ## K reversal potentail (mV)
    p['E_l'] = -17  ## Leak reversal potentail (mV)
    p['E_A'] = -75

    ## voltage dependence of gate variables    
    ### Na activation
    p['alpha_m'] = np.vectorize(
        lambda v: 0.38 * (v + 29.7) / (1. - np.exp(-(v + 29.7) * 0.1)))
    p['beta_m'] = lambda v: 15.2 * np.exp(-0.0556 * (v + 54.7))

    ### Na inactivation
    p['alpha_h'] = lambda v: 0.266 * np.exp(-0.05 * (v + 48.))
    p['beta_h'] = lambda v: 3.8 / (1. + np.exp(-0.1 * (v + 18.)))

    ### K activation
    p['alpha_n'] = np.vectorize(
        lambda v: 0.02 * (v + 45.7) / (1. - np.exp(-0.1 * (v + 45.7))))
    p['beta_n'] = lambda v: 0.25 * np.exp(-0.0125 * (v + 55.7))

    # Steven-connors addition
    p['a_inf'] = lambda v: (0.0761 * np.exp(0.0314 * (v + 94.22)) / (1 + np.exp(0.0346 * (v + 1.17))))**(1 / 3.0)
    p['tau_a'] = lambda v: 0.3632 + 1.158 / (1 + np.exp(0.0497 * (v + 55.96)))

    p['b_inf'] = lambda v: (1 / (1 + np.exp(0.0688 * (v + 53.3))))**4
    p['tau_b'] = lambda v: 1.24 + 2.678 / (1 + np.exp(0.0624 * (v + 50)))

    derived_parameters(p)  ## add derived parameters to dictionary (see below)

    ## HINT: Storing parameters in dictionaries simplifies function definitions by reducing number of arguments (see below).
    return p


##############################################################################################
def derived_parameters(p):
    '''
    Set derived parameters, i.e. parameters which are fully defined by parameters in p.

    Parameters:
    -----------
    p: dict
       Parameter dictionary
     
    Returns:
    --------
    nothing (p is modified "on-the-fly").
    
    '''

    p['time'] = np.arange(p['t_start'], p['T'] + p['dt'], p['dt']
                          )  ## time array (ms)
    p['n_inf'] = lambda v: p['alpha_n'](v) / (p['alpha_n'](v) + p['beta_n'](v))  ## steady-state K activation
    p['tau_n'] = lambda v: 1. / (p['alpha_n'](v) + p['beta_n'](v))  ## (ms)
    p['m_inf'] = lambda v: p['alpha_m'](v) / (p['alpha_m'](v) + p['beta_m'](v))  ## steady-state Na activation
    p['tau_m'] = lambda v: 1. / (p['alpha_m'](v) + p['beta_m'](v))  ## (ms)
    p['h_inf'] = lambda v: p['alpha_h'](v) / (p['alpha_h'](v) + p['beta_h'](v))  ## steady-state Na inactivation
    p['tau_h'] = lambda v: 1. / (p['alpha_h'](v) + p['beta_h'](v))  ## (ms)


##############################################################################################
def stimulus(p):
    '''
    Consctructs array I of input currents with

    I(t) = p['I_amp']        for p['t_stim_on'] <= t <= p['t_stim_off']
    I(t) = 0.0               else.

    (i.e. current pulse of length p['t_stim_off']-p['t_stim_on']).
    
    Parameters:
    -----------
    p: dict
       Parameter dictionary
     
    Returns:
    --------
    I: ndarray
       Array of input currents with with len(I) = len(p['time']).

    '''

    I = np.zeros(len(p['time']))
    N = len(p['time'])
    n = 0
    while (n < N):
        t = n * p['dt'] + p['time'][0]
        if t > p['t_stim_on'] and t < p['t_stim_off']:
            I[n] = p['I_amp']
        else:
            I[n] = 0

        n += 1

    return I


##############################################################################################
def update(Vm, m, h, n, a, b, I, p):
    '''
    Updates neuron state (Vm,m,h,n) from time step i-1 to time step i.

    Parameters:
    -----------
    Vm: float
        Membrane potentential at time step i-1.
     m: float
        Na activation at time step i-1.
     h: float
        Na inactivation at time step i-1.
     n: float
        K activation at time step i-1.
     I: float
        Input current at time step i-1.
     p: dict
        Parameter dictionary
    
    Returns:
    --------
    Vm: float
        Membrane potentential at time step i.
     m: float
        Na activation at time step i.
     h: float
        Na inactivation at time step i.    
     n: float
        K activation at time step i.
    '''

    Vm = Vm + p['dt']/p['Cm']*(\
            I  \
            - p['gbar_K'] *n**4*  (Vm - p['E_K'])       \
            - p['gbar_Na']*m**3*h*(Vm - p['E_Na'])      \
            - p['gbar_l'] *       (Vm - p['E_l'])       \
            - p['gbar_A'] *a**3*b*(Vm - p['E_A'])       \
            )
    m = m + p['dt'] * (p['m_inf'](Vm) - m) / p['tau_m'](Vm)
    h = h + p['dt'] * (p['h_inf'](Vm) - h) / p['tau_h'](Vm)
    n = n + p['dt'] * (p['n_inf'](Vm) - n) / p['tau_n'](Vm)
    a = a + p['dt'] * (p['a_inf'](Vm) - a) / p['tau_a'](Vm)
    b = b + p['dt'] * (p['b_inf'](Vm) - b) / p['tau_b'](Vm)
    return Vm, m, h, n, a, b


##############################################################################################
def simulate(p):
    '''
    1) Initialises state variables Vm, m, h, n with respective values at resting potential p['V_rest'].
    2) Constructs and returns array I of input currents by calling stimulus().
    3) Constructs array Vm of membrane potentials by calling update() in each time step.

    Parameters:
    -----------
    p: dict
       Parameter dictionary
       
    Returns:
    --------
    Vm: ndarray
        Array of membrane potentials with len(Vm) = len(p['time']).
     I: ndarray
        Array of input currents with len(I) = len(p['time']).

    '''

    Vm = np.zeros(len(p['time']))
    m = np.zeros(len(p['time']))
    h = np.zeros(len(p['time']))
    n = np.zeros(len(p['time']))
    a = np.zeros(len(p['time']))
    b = np.zeros(len(p['time']))

    Vm[0] = p['V_rest']
    m[0] = p['m_inf'](Vm[0])
    n[0] = p['n_inf'](Vm[0])
    h[0] = p['h_inf'](Vm[0])
    a[0] = p['a_inf'](Vm[0])
    b[0] = p['b_inf'](Vm[0])

    # print 'Inital Values:'
    # print 'Vm : ', Vm[0]
    # print 'm : ', m[0]
    # print 'h : ', h[0]
    # print 'n : ', n[0]
    # print 'a : ', a[0]
    # print 'b : ', b[0]

    I = stimulus(p)

    spikes = 0
    sIndex = -1
    N = len(p['time'])
    i = 0
    while (i < N - 1):
        Vm[i+1], m[i+1], h[i+1] , n[i+1], a[i+1], b[i+1] \
            = update(Vm[i], m[i], h[i], n[i],a[i], b[i], I[i], p)
        i += 1

    # print 'End Values:'
    # print 'Vm : ', Vm[-1]
    # print 'm : ', m[-1]
    # print 'h : ', h[-1]
    # print 'n : ', n[-1]
    # print 'a : ', a[-1]
    # print 'b : ', b[-1]

    return Vm, I


def find_threshold_and_plot():
    n = 20
    amp = np.linspace(7.5, 12, n)
    firing_rate = np.zeros([n])
    spike_cnt = 0
    threshold = 0
    for i, a in enumerate(amp):
        print 'Simulating...'
        p = set_parameters_sweep(a)

        Vm, I = simulate(p)

        # Remove the preparation part of the signal.
        I = I[int(-p['t_start'] / p['dt']):-1]
        Vm = Vm[int(-p['t_start'] / p['dt']):-1]
        p['time'] = p['time'][int(-p['t_start'] / p['dt']):-1]

        # Find local maxima.
        max_idx = argrelextrema(Vm, np.greater)[0]
        # # Remove strange empty elements.
        max_idx = filter(None, max_idx)
        # Count local maxima over threshold as spikes.
        Vm_max = Vm[max_idx]
        for idx in xrange(len(Vm_max)):
            if Vm_max[idx] < threshold:
                np.delete(Vm_max, idx)
                np.delete(max_idx, idx)
        if len(max_idx) > 2:
            T_vec = np.diff(max_idx) * p['dt']
            T = float(np.sum(T_vec)) / len(T_vec)
            firing_rate[i] = 1.0 / T * 1000
        else:
            firing_rate[i] = 0
        # spike_cnt = np.sum(Vm_max >= threshold)
        # firing_rate[i] = float(spike_cnt)/p['T']*1000
        # plt.plot(amp,firing_rate)
        # plt.show()

        # Find the threshold.
    threshold = 0
    if firing_rate[0] != 0:
        print 'Warning: Cannot find threshold. Continuing without.'
    else:
        for i in xrange(len(amp)):
            if firing_rate[i] != 0:
                threshold = amp[i - 1]
                break
    return threshold, firing_rate, amp

##############################################################################################
##############################################################################################
## main program

if __name__ == "__main__":
    p = set_parameters_sweep(0)

    thresh, f, amp = find_threshold_and_plot()
    LFPy_util.plot.frequency_amp(f, amp, fname='threshold', show=False)
    LFPy_util.plot.frequency_amp(f,
                                 amp,
                                 relative=True,
                                 fname='threshold_relative',
                                 show=False)
    info_file = open('threshold_info.md', 'w')
    info_file.write('threshold = {}\n'.format(thresh))
    info_file.write('dt = {}\n'.format(p['dt']))
    info_file.close()
