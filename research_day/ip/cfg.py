""" cfg.py """
import sys
sys.path.append('../..')
from netpyne import specs
import numpy as np
from itertools import product

cfg = specs.SimConfig()  

cfg.dt = 0.0125
cfg.cvode_active = False
cfg.recordStims = False
cfg.recordStep = 0.5

cfg.delay = 300
cfg.isis = (1000 / np.arange(3, 11, 1)).round(1)
cfg.amp = 1.6
cfg.width = 0.5
cfg.duration = 500

cfg.recordCells = ['all']

for var in [ 'v', 'ina', 'ik', 'ica', 'icl']:
    cfg.recordTraces[var] = {'sec': 'soma', 'loc': 0.5, 'var': '%s' %(var)}

for label, var in [ ['NaV1.7', 'ina_nav1p7'], ['NaV1.8', 'ina_nav1p8'], ['KA', 'ik_kas'], ['KDR', 'ik_kdr'] ]:
    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': var}

# Saving
cfg.simLabel = 'sim'
cfg.saveFolder = 'data'
cfg.savePickle = True

# run simulation
cfg.hParams = {'celsius': 22}

cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'trace', 'saveData': True, 'saveFig': True,
                           'showFig': False, 'timeRange': [0, cfg.duration]}

#use the saveData to plot values
