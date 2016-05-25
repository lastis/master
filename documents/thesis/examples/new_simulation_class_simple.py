from LFPy_util.sims import Simulation

class CustomSimulation(Simulation):
    def __init__(self):
        # Inherit the LFPyUtil simulation class.
        Simulation.__init__(self)
        # These values are used by the super class to save and load
        # data and run_param.
        self.name           = "custom_sim"
        self.name_save_load = "custom_sim"

    def simulate(self, cell):
        pass

    def process_data(self):
        pass

    def plot(self, dir_plot):
        pass
