import LFPy
import LFPy_util
import matplotlib.pyplot as plt
from LFPy_util.sims import Simulation

class CustomSimulation(Simulation):
    def __init__(self):
        """
        Typical initialization function, called when a new instance 
        is created.
        """
        # Inherit the LFPyUtil simulation class.
        Simulation.__init__(self)
        # These values are used by the super class to save and load data.
        self.set_name("custom_sim")

        # Create some parameters that are used by the simulate method.
        self.run_param['delay'] = 100       # ms.
        self.run_param['duration'] = 300    # ms.
        self.run_param['amp'] = 1.0         # nA.

        # Create a parameters used by the plotting function.
        self.plot_param['plot_norm'] = True

    def simulate(self, cell):
        """
        Setup and starts a simulation, then gathers data.

        :param LFPy.Cell cell:
            Cell object from LFPy.
        """
        # Create an electrode with LFPy.
        soma_clamp_params = {
            'idx': cell.somaidx,
            'amp': self.run_param['amp'],
            'dur': self.run_param['duration'],
            'delay': self.run_param['delay'],
            'pptype': 'IClamp'
        }
        stim = LFPy.StimIntElectrode(cell, **soma_clamp_params)

        cell.simulate()

        # Store the data .
        self.data['soma_v'] = cell.somav
        self.data['soma_t'] = cell.tvec

    def process_data(self):
        """
        Process data from the simulate function, usually to prepare
        the data for plotting. This function creates a normalized 
        version of the membrane potential.
        """
        soma_v_norm = self.data['soma_v'].copy()
        soma_v_norm -= soma_v_norm[0]
        soma_v_norm /= soma_v_norm.max()
        self.data['soma_v_norm'] = soma_v_norm

    def plot(self, dir_plot):
        """
        Plot data from the simulate and process_data function.
        This functions plots the membrane potential and the 
        normalized version.

        :param string dir_plot:
            Path to the directory where plots should be saved. 
        """
        plt.plot(self.data['soma_t'], self.data['soma_v'])
        # Save the plot to input directory with the name "custom_sim_mem".
        LFPy_util.plot.save_plt(plt, "custom_sim_mem", dir_plot)
        # plot_param can be used to affect the plotting.
        if self.plot_param['plot_norm']:
            plt.plot(self.data['soma_t'], self.data['soma_v_norm'])
            # Save the plot to input directory.
            LFPy_util.plot.save_plt(plt, "custom_sim_mem_norm", dir_plot)
