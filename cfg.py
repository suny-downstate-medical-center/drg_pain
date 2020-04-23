""" cfg.py """
from netpyne import specs

cfg = specs.SimConfig()  

#simulation parameters
#cfg.dt = 0.0125
cfg.cvode_active = True
cfg.recordStims = False
cfg.recordStep = 0.5

#modify values
#mechs['nav18']['gnabar'] = 0
#netParam parameters
cfg.secs = {'drgperi': {'nseg':257, 'L':5000,  'diam': 0.8 },
            'drgstem': {'nseg':3,   'L':75,    'diam': 1.4 },
            'drgsoma': {'nseg':1,   'L':30,    'diam': 23  },
            'drgcntr': {'nseg':363, 'L':5000,  'diam': 0.4 }}

nav17 = cfg.nav17 = 'nav17m'
nav18 = cfg.nav18 = 'nav18m'

# section mechanisms
cfg.mechs = {nav17   : {'gnabar': 0.018 },
             nav18   : {'gnabar': 0.026 },
             'kdr'   : {'gkbar' : 0.0035},
             'ka'    : {'gkbar' : 0.0055},
             'pas'   : {'g': 5.75e-5, 'e': -58.91}}

# ion reversal potentials
cfg.ions  = {'na':  67.1,
             'k' : -84.7 }

# section properties
cfg.props = {'cm': 1.2,
             'Ra': 123}

# simplified connection list
cfg.cons = (('drgstem', 'drgperi'),
            ('drgsoma', 'drgstem'),
            ('drgcntr', 'drgperi'))

#without plot traces, this is necessary
cfg.recordCells = ['all']

for label, chan in [ ['NaV1.7', nav17], ['NaV1.8', nav18] ]:
    cfg.recordTraces[label] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}

for label, chan in [ ['KDR','kdr'], ['KA','ka'] ]:
    cfg.recordTraces[label] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'ik_%s' %(chan)}

#generate recordTraces of peri, soma, cntr
for label, sec in [ ['v_peri', 'drgperi'], ['v_soma', 'drgsoma'], ['v_cntr', 'drgcntr'] ]:
    cfg.recordTraces[label] = {'sec': sec, 'loc': 0.5, 'var': 'v'}

cfg.recordTraces['mtau'] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'minf_nav18m'}
cfg.recordTraces['htau'] = {'sec': 'drgsoma', 'loc': 0.5, 'var': 'hinf_nav18m'}

"""
#generate recordTraces along the fiber
for x in range(6):
    x = x * 0.2
#vt+0.0 is the same entry so we can avoid a duplicate trace at the t-junction
    cfg.recordTraces['v_fiber%+1.1f' %(0-x)] = {'sec': 'drgperi', 'loc': (1-x), 'var': 'v'}
    cfg.recordTraces['v_fiber%+1.1f' %(x  )] = {'sec': 'drgcntr', 'loc': x    , 'var': 'v'}
"""

# Saving
cfg.simLabel = 'sim1'
cfg.saveFolder = 'data'
cfg.savePickle = True
# cfg.saveJson = True
cfg.saveDataInclude = ['simData']

# run simulation
cfg.hParams = {'celsius': 22, 'v_init': cfg.mechs['pas']['e']}
cfg.duration = 300
cfg.delay    = 100
"""
cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'cell', 'saveData': True, 'saveFig': True,#'plots/n7_%.1f_n9_%.3f_k2_%.3f_k3_%.3f.png' %(cfg.nacndct[0], cfg.gna19, cfg.gk2, cfg.gk3),
                           'showFig': False, 'timeRange': [0, cfg.duration]}
"""
#use the saveData to plot values