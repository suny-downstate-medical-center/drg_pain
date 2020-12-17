from netpyne import sim
from itertools import product
from npvec import npvec
import numpy as np
import matplotlib.pyplot as plt

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

# store stims in dictionary
stimd = { 'ic': {},'vc': {},'pls': {} }

# for vstim in cfg.vstims:
#     vclampv = npvec(cfg.duration, cfg.dt, -60)
#     vclampv.plsf(cfg.dur[0], cfg.dur[1], vstim)
#     stimd['v'][vstim] = sim.h.Vector(vclampv.vector)

for isi in cfg.isis:
    ipulse = npvec(cfg.duration, cfg.dt, 0)
    deltas = []
    delta = cfg.dur[0]
    while delta < cfg.duration:
        deltas.append(delta)
        delta = delta + isi
    ipulse.plsf_train(deltas, 5, 0.25)
    stimd['pls'][isi] = sim.h.Vector(ipulse.vector)
# last iclampv t used (all same)
t = sim.h.Vector(ipulse.t)

# Choi
# Membrane potential was set by constant current injection
# (−13.74 pA for −70 mV, −7.24 pA for −65 mV, 9.55 pA for −55 mV, and 25.64 pA for −50 mV)
"""
for cell in sim.net.cells:
    tags = cell.tags['cellType']
    if tags['stim'] == 'pls':
        stimd['pls'][tags['val']].play(cell.stims[0]['hObj']._ref_amp, t, True)
"""
sim.simulate() # calls runSim() and gatherData()
sim.analyze()
