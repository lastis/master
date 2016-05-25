# Import the get_cell function defined previously.
from load_model import get_cell

# Import the newly defined simulation class.
from new_simulation_class import CustomSimulation

# Load the model, using a string to identify which model will be returned.
cell = get_cell("pyramidal_1")

# Create an instance of the custom simulation class.
sim = CustomSimulation()

sim.simulate(cell)
sim.process_data()
sim.plot(".")

