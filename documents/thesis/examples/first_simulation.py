# Import the get_cell function defined previously.
from load_model import get_cell

# Import the newly defined simulation class.
from new_simulation_class import CustomSimulation

# Load the model, using a string to identify which model will be returned.
cell = get_cell("pyramidal_1")

# Create an instance of the custom simulation class.
sim_custom = CustomSimulation()

sim_custom.simulate(cell)
sim_custom.process_data()
# Plots are stored in a folder called first_simulation.
sim_custom.plot("first_simulation")
