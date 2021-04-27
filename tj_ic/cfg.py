""" cfg.py """
import sys
sys.path.append('..')
from netpyne import specs
import numpy as np
from itertools import product

cfg = specs.SimConfig()

cfg.dt = 0.025
cfg.cvode_active = False
cfg.recordStims = False
cfg.recordStep = 0.5

cfg.delay = 100
cfg.isis = (1000 / np.array([ 5, 10, 15, 20 ])).round(1)
cfg.isis = [1000 / 50]
cfg.amps = np.linspace(0.1, 0.2, 20) #[ 0.20, 0.21, 0.22, 0.23, 0.24, 0.25 ]
#muts default to 0, muls default to 1
cfg.muls = np.linspace(0, 1, 5)
cfg.muts = [0.0] #[ 0.5,  0.6,  0.7,  0.8,  0.9,  1.0  ]
cfg.ashfts = [0.0] # positive sign shifts curve to left ( activates at lower voltages)
cfg.ishfts = [0.0]
cfg.width = 1
cfg.duration = 3100

cfg.recordCells = ['all']

# for var, loc in product([ 'v', 'ina', 'ik', 'i_pas'], np.linspace(0, 1, 5)):
#     cfg.recordTraces["%s(%s)" %(var, loc)] = {'sec': 'cable', 'loc': loc, 'var': '%s' %(var)}

for var, loc in product(['v'], np.linspace(0.1, 0.9, 9) ):
    cfg.recordTraces["peri %s(%s)" %(var, loc)] = {'sec': 'cblperi', 'loc': loc, 'var': '%s' %(var)}

cfg.recordTraces["tj v(0.0)"] = {'sec': 'cblperi', 'loc': 1.0, 'var': 'v'}

for var, loc in product(['v'], np.linspace(0.1, 0.5, 5) ):
    cfg.recordTraces["cntr %s(%s)" %(var, loc)] = {'sec': 'cblcntr', 'loc': loc, 'var': '%s' %(var)}

# cfg.recordTraces["n1p7_ina_peri"] = {'sec': 'cblperi', 'loc': 0.5, 'var': 'ina_nav1p7'}
# cfg.recordTraces["n1p7_ina_tj"  ] = {'sec': 'cblperi', 'loc': 1.0, 'var': 'ina_nav1p7'}
# cfg.recordTraces["n1p7_ina_cntr"] = {'sec': 'cblcntr', 'loc': 0.5, 'var': 'ina_nav1p7'}
#
# cfg.recordTraces["n1p8_ina_peri"] = {'sec': 'cblperi', 'loc': 0.5, 'var': 'ina_nav1p8'}
# cfg.recordTraces["n1p8_ina_tj"  ] = {'sec': 'cblperi', 'loc': 1.0, 'var': 'ina_nav1p8'}
# cfg.recordTraces["n1p8_ina_cntr"] = {'sec': 'cblcntr', 'loc': 0.5, 'var': 'ina_nav1p8'}

# cfg.recordTraces["v_peri"] = {'sec': 'cblperi', 'loc': 0.5, 'var': 'v'}
# cfg.recordTraces["v_tj"  ] = {'sec': 'cblperi', 'loc': 1.0, 'var': 'v'}
# cfg.recordTraces["v_cntr"] = {'sec': 'cblcntr', 'loc': 0.5, 'var': 'v'}

# for var in [ 'v' ]:
#     cfg.recordTraces["drgsoma(%s)" % (var)] = {'sec': 'drgsoma', 'loc': 0.5, 'var': '%s' % (var)}

# for label, var in [ ['NaV1.7', 'ina_nav1p7'], ['NaV1.8', 'ina_nav1p8'], ['KA', 'ik_kas'], ['KDR', 'ik_kdr'] ]:
#     cfg.recordTraces[label] = {'sec': 'cable', 'loc': 0.25, 'var': var}

# Saving
cfg.simLabel = 'sim'
cfg.saveFolder = 'data'
cfg.savePickle = True

# run simulation
cfg.hParams = {'celsius': 37}

cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'trace', 'saveData': True, 'saveFig': True,
                           'showFig': False, 'timeRange': [20, cfg.duration]}

#use the saveData to plot values
