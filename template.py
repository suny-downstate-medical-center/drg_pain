"""
cfgtmp.py
a cfg template for ease of use with bash and sed scripts
"""
from netpyne import specs

cfg = specs.SimConfig()  

#simulation parameters (fixed timestep)
#cfg.dt = 0.0125
#cfg.cvode_active = False
cfg.cvode_active = True
cfg.recordStims = False
cfg.recordStep = 0.5

#netParam vars
cfg.freq = CFGFREQ
cfg.npulses = CFGNPULSES
cfg.amp = CFGAMP
cfg.dur = CFGDUR
cfg.mttxs = CFGMTTXS
cfg.mn1p8 = CFGMN1P8
cfg.mn1p9 = CFGMN1P9

#in case plotTraces does not get called -- need to specify to record from all cells
cfg.recordCells = ['all']

#simple plot traces
cfg.recordTraces['stim'] = {'sec': 'peri', 'loc': 0.0, 'var': 'v'}
#cfg.recordTraces['junction'] = {'sec': 'peri', 'loc': 1.0, 'var': 'v'}
cfg.recordTraces['soma'] = {'sec': 'soma', 'loc': 0.5, 'var': 'v'}
cfg.recordTraces['terminal'] = {'sec': 'cntr', 'loc': 1.0, 'var': 'v'}

#more plot traces
"""
for label, chan in [ ['NaV1.7', 'nattxs'], ['NaV1.8', 'nav1p8'] ]:
    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}

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
cfg.simLabel = 'CFGSIMLABEL'
cfg.saveFolder = 'data'
cfg.savePickle = True
# cfg.saveJson = True
cfg.saveDataInclude = ['simData']

# run simulation
cfg.hParams = {'celsius': 22, 'v_init': -53.5}

cfg.duration = 1000/cfg.freq * cfg.npulses + 100

cfg.analysis.plotTraces = {'include': ['all'], 'overlay': True, 'oneFigPer': 'cell', 'saveData': True, 'saveFig': True,
                           'showFig': False, 'timeRange': [0, cfg.duration]}

#use the saveData to plot values