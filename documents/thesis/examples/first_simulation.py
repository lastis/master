"""
Load a model and run a predefined simulation.
"""

import LFPy_util
import os
from load_model import get_cell

# Define a string that will identify the model that will be loaded.
neuron_name = "pyramidal_1"

# Define a path to an output folder. Here we choose the output 
# folder to have same name as the name of the neuron.
current_dir = os.path.dirname(os.path.realpath(__file__))
dir_plot = os.path.join(current_dir, neuron_name)

# Load the model.
cell = get_cell(neuron_name)

# Create an instance of one of the predefined simulation classes.
# This spesific simulation inserts an electrode that 
# excites the neuron until it fires 3 times. 
sim = LFPy_util.sims.MultiSpike()

# Run parameters and the output/results are stored 
# in the dictionaries:
#   sim.run_param
#   sim.data

# Run the simulation.
sim.simulate(cell)

# Process the results so it can be plotted and store the plots 
# to the output folder.
sim.process_data()
sim.plot(dir_plot)

