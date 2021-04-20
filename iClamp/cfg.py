""" cfg.py """
import sys
sys.path.append('..')
from netpyne import specs
import numpy as np
from itertools import product

cfg = specs.SimConfig()  

cfg.dt = 0.0125
cfg.cvode_active = False
cfg.recordStims = False
cfg.recordStep = 0.05

cfg.istims = np.arange(1.5, 1.8, 0.1)
cfg.dur = [250, 0.5]
cfg.duration = 300

cfg.recordCells = ['all']

for var in [ 'v', 'ina', 'ik', 'ica', 'icl']:
    cfg.recordTraces[var] = {'sec': 'soma', 'loc': 0.5, 'var': '%s' %(var)}

for label, var in [ ['NaV1.7', 'ina_nav1p7'], ['NaV1.8', 'ina_nav1p8'], ['KAs', 'ik_kaslow'], ['KA', 'ik_kas'], ['KDR', 'ik_kdr'] ]:
    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': var}

# Saving
cfg.simLabel = 'sim'
cfg.saveFolder = 'data'
cfg.savePickle = True

# run simulation
cfg.hParams = {'celsius': 22}

cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'trace', 'saveData': True, 'saveFig': True,
                           'showFig': False, 'timeRange': [252, 255]}

#use the saveData to plot values
