import sys
sys.path.append('..')
from netpyne import sim
from itertools import product
from npvec import npvec
import numpy as np
import matplotlib.pyplot as plt

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

# store stims in dictionary
# Choi
# Membrane potential was set by constant current injection
# (−13.74 pA for −70 mV, −7.24 pA for −65 mV, 9.55 pA for −55 mV, and 25.64 pA for −50 mV)

sim.simulate() # calls runSim() and gatherData()
sim.analyze()
