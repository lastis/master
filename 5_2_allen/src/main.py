import Simulation
import Model
import sys

argv = sys.argv[1:]
if len(argv) == 0 or argv[0] == 'run':
    cell = Model.init()
    Simulation.run(cell)
if len(argv) > 0 and argv[0] == 'plot':
    Simulation.plot()

