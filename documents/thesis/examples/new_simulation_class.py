from LFPy_util.sim import Simulation

class CustomSimulation(Simulation):
    def __init__(self):
        Simulation.__init__(self)
        # Used by the super save and load function.
        self.set_name('stim_electrode')

        # Used by the custom simulate and plot function.
        self.run_param['delay'] = 100
        self.run_param['duration'] = 300
        self.run_param['amp'] = 0.1

    def simulate(self, cell):
        pass

    def process_data(self):
        pass

    def plot(self, dir_plot):
        data = self.data
