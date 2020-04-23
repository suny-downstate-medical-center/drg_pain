from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg
from cellcopy import dcp, cell_copy

vrest, delay = cfg.hParams['v_init'], cfg.delay
secs, props, mechs, ions, cons, nav17, nav18 = cfg.secs, cfg.props, cfg.mechs, cfg.ions, cfg.cons, cfg.nav17, cfg.nav18

numcells = 3
# calculate stimulus based on index
cs = lambda i: (i + 1.0)/numcells
# NetParams object to store network parameters
netParams = specs.NetParams()   # object of class NetParams to store the network parameters

# tjargs and sargs, sargs consisting of just soma.
# note that these are all shallow copies...
tjargs = {'secs': secs, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': cons}
sargs  = {'secs': {'drgsoma': secs['drgsoma']}, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': ()}

# changing parameters in tjargs and sargs will be universal -- e.g.
mechs[nav18]['gnabar'] = 1

# make deep copies
tjargs = dcp(tjargs)
sargs  = dcp(sargs)

# import cell parameters
tjParams = netParams.importCellParams(label = 'foo', conds={'bar':'baz'}, fileName='genrn.py' , cellName='genrn' , cellArgs=tjargs)
sParams  = netParams.importCellParams(label = 'foo', conds={'bar':'baz'}, fileName='genrn.py' , cellName='genrn' , cellArgs=sargs )
# strip condition parameters
del tjParams['conds']
del sParams['conds']

# set up cell and voltage clamp
vc = 'vccnrn'
netParams.popParams[vc] = {'numCells': 1, 'cellModel': vc}
vcLblParams = {'conds':{'cellModel': vc}, **sParams}
netParams.cellParams[vc] = vcLblParams

netParams.stimSourceParams[vc] = {'type': 'SEClamp', 'dur1': delay, 'dur2': delay, 'dur3': 0,  'amp1': vrest,  'amp2': 0,  'amp3': 0 }
netParams.stimTargetParams[vc] = {'source': vc, 'conds': {'cellModel': vc}, 'sec': 'drgsoma', 'loc': 0.5}


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

    stimstr = 'iclamp%d' %(i)

# current clamp -- around 0.5 nA
    netParams.stimSourceParams[stimstr] = {'type': 'IClamp', 'delay': cfg.delay, 'dur': 2.5, 'amp': cs(i)}
    netParams.stimTargetParams[stimstr + tjlbl] = {'source': stimstr, 'conds': {'cellModel': tjlbl }, 'sec': 'drgperi', 'loc': 0.0}
    netParams.stimTargetParams[stimstr + slbl ] = {'source': stimstr, 'conds': {'cellModel': slbl  }, 'sec': 'drgsoma', 'loc': 0.5}

# voltage clamp
'''
    netParams.stimSourceParams[stimstr] = {'type': 'VClamp', 'dur': [delay, 2.5, 2.5], 'amp': [-57, 10, -57]}    
    netParams.stimTargetParams[stimstr] = {'source': stimstr, 'conds': {'popLabel': 'cnrn'}, 'sec': 'drgsoma', 'loc': 0.5}
'''