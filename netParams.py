from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg
from copy import deepcopy as dcp
numcells = 3
# calculate stimulus based on index
cs = lambda i: (i + 1.0)/numcells
# NetParams object to store network parameters
netParams = specs.NetParams()   # object of class NetParams to store the network parameters

# tjargs and sargs, sargs consisting of just soma.
# note that these are all shallow copies...
tjargs = {'secs': cfg.secs, 'props': cfg.props, 'mechs': cfg.mechs, 'ions': cfg.ions, 'cons': cfg.cons}
sargs  = {'secs': {'drgsoma': cfg.secs['drgsoma']}, 'props': cfg.props, 'mechs': cfg.mechs, 'ions': cfg.ions, 'cons': ()}

# change parameter referenced by tjargs and sargs universally through cfg. e.g.
# cfg.mechs['nav18']['gnabar'] = cfg.mechs['nav18']['gnabar'] * 0.5

# import cell parameters
tjParams = netParams.importCellParams(label = 'foo', conds={'bar':'baz'}, fileName='genrn.py' , cellName='genrn' , cellArgs=tjargs)
sParams  = netParams.importCellParams(label = 'foo', conds={'bar':'baz'}, fileName='genrn.py' , cellName='genrn' , cellArgs=sargs )
# strip condition parameters
del tjParams['conds']
del sParams['conds']
# change local parameters to tjParams, sParams

# set up voltage clamp
vc = 'vccnrn'
netParams.popParams[vc] = {'numCells': 1, 'cellModel': vc}
vcLblParams = {'conds':{'cellModel': vc}, **sParams}
netParams.cellParams[vc] = vcLblParams
brk = 1
# set up current clamps
for i in range(numcells):

# create unique tag strings
    cstr  = 'cnrn%d' %(i)
    tjlbl = 'tjcnrn%d' %(i)
    slbl  = 'scnrn%d' %(i)

# tags:
# cellType of cnrn<x>, cellModel either is tjunction<x>, or only soma<x>.
    netParams.popParams[tjlbl] = {'numCells': 1, 'cellModel': tjlbl }
    netParams.popParams[slbl]  = {'numCells': 1, 'cellModel': slbl  }

# assign conds for cell parameters
    tjLblParams = {'conds':{'cellModel': tjlbl}, **tjParams}
    sLblParams  = {'conds':{'cellModel':  slbl}, **sParams }
# assign cell parameters
    netParams.cellParams[tjlbl] = tjLblParams
    netParams.cellParams[slbl]  = sLblParams

    tjParams['secs']['drgsoma']['geom']['L'] = 100000

    stimstr = 'iclamp%d' %(i)

# current clamp -- around 0.5 nA
    netParams.stimSourceParams[stimstr] = {'type': 'IClamp', 'delay': cfg.delay, 'dur': 2.5, 'amp': cs(i)}
    netParams.stimTargetParams[stimstr + tjlbl] = {'source': stimstr, 'conds': {'cellModel': tjlbl }, 'sec': 'drgperi', 'loc': 0.0}
    netParams.stimTargetParams[stimstr + slbl ] = {'source': stimstr, 'conds': {'cellModel': slbl  }, 'sec': 'drgsoma', 'loc': 0.0}

# voltage clamp
'''
    netParams.stimSourceParams[stimstr] = {'type': 'VClamp', 'dur': [delay, 2.5, 2.5], 'amp': [-57, 10, -57]}    
    netParams.stimTargetParams[stimstr] = {'source': stimstr, 'conds': {'popLabel': 'cnrn'}, 'sec': 'drgsoma', 'loc': 0.5}
'''