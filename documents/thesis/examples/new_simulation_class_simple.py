from LFPy_util.sims import Simulation

class CustomSimulation(Simulation):
    def __init__(self):
        # Inherit the LFPyUtil simulation class.
        Simulation.__init__(self)
        # These values are used by the super class to save and load data.
        self.set_name("custom_sim")

    def simulate(self, cell):
        pass

    def process_data(self):
        pass

    def plot(self, dir_plot):
        pass
