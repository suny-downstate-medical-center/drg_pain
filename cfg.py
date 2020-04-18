""" cfg.py """
from netpyne import specs
from netpyne.specs import Dict, ODict

from genrn import secs, props, mechs, ions, cons

cfg = specs.SimConfig()  

#simulation parameters
cfg.hParams = {'celsius': 22, 'v_init': mechs['pas']['e']}
#cfg.dt = 0.0125
cfg.cvode_active = True
cfg.recordStims = False
cfg.recordStep = 0.5

#modify values
#mechs['nav18']['gnabar'] = 0
#netParam parameters
cfg.secs  = secs
cfg.props = props
cfg.mechs = mechs
cfg.ions  = ions
cfg.cons  = cons

#generate recordTraces for the peripheral axon, note that will be in centimeters
"""
#generate recordTraces along the fiber
for x in range(6):
    x = x * 0.2
#vt+0.0 is the same entry so we can avoid a duplicate trace at the t-junction
    cfg.recordTraces['v_fiber%+1.1f' %(0-x)] = {'sec': 'drgperi', 'loc': (1-x), 'var': 'v'}
    cfg.recordTraces['v_fiber%+1.1f' %(x  )] = {'sec': 'drgcntr', 'loc': x    , 'var': 'v'}


for label, chan in [ ['NaV1.7','nav17'], ['NaV1.8','nav18'] ]:
    cfg.recordTraces[label] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}

for label, chan in [ ['kdr','kdr'], ['ka','ka'] ]:
    cfg.recordTraces[label] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_%s' %(chan)}

#generate recordTraces of peri, soma, cntr
for label, sec in [ ['v_peri', 'drgperi'], ['v_soma', 'drgsoma'], ['v_cntr', 'drgcntr'] ]:
    cfg.recordTraces[label] = {'sec': sec, 'loc': 0.5, 'var': 'v'}
"""

cfg.recordTraces['mtau'] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'minf_nav18'}
cfg.recordTraces['htau'] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'hinf_nav18'}

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = True
# cfg.saveJson = True
cfg.saveDataInclude = ['simData']

cfg.duration = 200
cfg.delay    = 100
cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'cell', 'saveData': True, 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3),
                           'showFig': False, 'timeRange': [0, cfg.duration]}

#use the saveData to plot values