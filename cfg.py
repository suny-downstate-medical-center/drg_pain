""" cfg.py """
from netpyne import specs
import numpy as np


cfg = specs.SimConfig()  

#simulation parameters (fixed timestep)
#cfg.dt = 0.0125
#cfg.cvode_active = False
cfg.cvode_active = False
cfg.recordStims = False
cfg.recordStep = 0.0125

#cfg.v_inits = np.linspace( -80, -40, 21)
#cfg.stims = np.linspace( 0, 0.5, 21)
cfg.v_inits = [-70, -60, -50]
cfg.stims = [0.12, 0.25, 0.37]
cfg.duration = 1500

cfg.recordCells = ['all']

for var in [ 'v', 'i_pas', 'h', 'ina', 'ik', 'ica', 'icl']:
    cfg.recordTraces[var] = {'sec': 'soma', 'loc': 0.5, 'var': '%s' %(var)}

for label, nav in [ ['NaV1.7', 'nattxs'], ['NaV1.8', 'nav1p8'] ]:
    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': 'ina_%s' %(nav)}

"""
pts = 3
#generate recordTraces along the fiber and at soma (ordered dictionary so generate them in order)
for x in range(-pts, 0):
    x /= pts
    cfg.recordTraces['v_fiber(%+1.2f)' %(x)] = {'sec': 'peri', 'loc': (1+x), 'var': 'v'}

for x in range(0, pts+1):
    x /= pts
    cfg.recordTraces['v_fiber(%+1.2f)' %(x)] = {'sec': 'cntr', 'loc': x    , 'var': 'v'}
    
cfg.recordTraces['v_soma'] = {'sec': 'soma', 'loc': 0.5, 'var': 'v'}
"""
# Saving
cfg.simLabel = 'simtest'
cfg.saveFolder = 'data'
cfg.savePickle = True
cfg.saveJson = True
# cfg.saveDataInclude = ['netParams', 'netCells', 'simData', 'simConfig', 'plotData']

# run simulation
cfg.hParams = {'celsius': 22}

cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'trace', 'saveData': True, 'saveFig': True,
                           'showFig': False, 'timeRange': [0, cfg.duration]}

#use the saveData to plot values
