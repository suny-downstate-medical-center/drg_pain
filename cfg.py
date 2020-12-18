""" cfg.py """
from netpyne import specs
import numpy as np
from itertools import product

cfg = specs.SimConfig()  

cfg.dt = 0.0125
cfg.cvode_active = False
cfg.recordStims = False
cfg.recordStep = 0.5

cfg.istims = np.linspace(0.00, 0.4, 21)
cfg.vstims = np.linspace(0, 100, 21)
cfg.isis = [100, 125, 167, 250, 333, 500]
cfg.isis = [100]
cfg.dur = [250, 1000]
cfg.duration = 1250

cfg.recordCells = ['all']
"""
for var in [ 'v', 'ina', 'ik', 'ica', 'icl']:
    cfg.recordTraces[var] = {'sec': 'soma', 'loc': 0.5, 'var': '%s' %(var)}
#for var in [ 'v', 'i_pas', 'h', 'ina', 'ik', 'ica', 'icl']:

for label, nav in [ ['NaV1.7', 'nav1p7'], ['NaV1.8', 'nav1p8'], ['NaV1.8T', 'nav1p8T'] ]:
    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': 'ina_%s' %(nav)}
"""
for var in [ 'v' ]:
    for sec, loc in [ ['cblperi', 0], ['cblperi', 0.5], ['cblperi', 1.0], ['drgsoma', 0.5], ['cblcntr', 0.5], ['cblcntr', 1.0]]:
        label = "%s(%s).%s" %(sec, loc, var)
        cfg.recordTraces[label] = {'sec': sec, 'loc': loc, 'var': '%s' %(var)}

for var in [ 'ina', 'ik', 'i_pas' ]:
    for sec, loc in [ ['cblperi', 0], ['cblperi', 0.5], ['cblperi', 1.0], ['drgsoma', 0.5], ['cblcntr', 0.5], ['cblcntr', 1.0]]:
        label = "%s(%s).%s" %(sec, loc, var)
        cfg.recordTraces[label] = {'sec': sec, 'loc': loc, 'var': '%s' %(var)}

for var in [ 'v' ]:
    for sec, loc in [ ['cable', 0], ['cable', 0.25], ['cable', 0.5], ['cable', 0.75], ['cable', 1.00] ]:
        label = "%s(%s).%s" % (sec, loc, var)
        cfg.recordTraces[label] = {'sec': sec, 'loc': loc, 'var': '%s' %(var)}

for var in [ 'ina', 'ik', 'i_pas' ]:
    for sec, loc in [ ['cable', 0], ['cable', 0.25], ['cable', 0.5], ['cable', 0.75], ['cable', 1.00] ]:
        label = "%s(%s).%s" %(sec, loc, var)
        cfg.recordTraces[label] = {'sec': sec, 'loc': loc, 'var': '%s' %(var)}

# Saving
cfg.simLabel = 'sim'
cfg.saveFolder = 'data'
cfg.savePickle = True
# cfg.saveJson = True
# cfg.saveDataInclude = ['netParams', 'netCells', 'simData', 'simConfig', 'plotData']

# run simulation
cfg.hParams = {'celsius': 22}

cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'trace', 'saveData': True, 'saveFig': True,
                           'showFig': False, 'timeRange': [0, cfg.duration]}

#use the saveData to plot values

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
