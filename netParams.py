from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg

numcells = 5
# calculate stimulus based on index
cs = lambda i: (i + 1)/numcells
# NetParams object to store network parameters
netParams = specs.NetParams()   # object of class NetParams to store the network parameters

tjargs = {'secs': cfg.secs, 'props': cfg.props, 'mechs': cfg.mechs, 'ions': cfg.ions, 'cons': cfg.cons}
sargs  = {'secs': {'drgsoma': cfg.secs['drgsoma']}, 'props': cfg.props, 'mechs': cfg.mechs, 'ions': cfg.ions, 'cons': ()}

# set up voltage clamps

# set up current clamps
for i in range(numcells):

# create unique tag strings
    cstr  = 'cnrn%d' %(i)
    tjlbl = 'tjcnrn%d' %(i)
    slbl  = 'scnrn%d' %(i)

# tags:
# cellType of cnrn<x>, cellModel either is tjunction<x>, or only soma<x>.
    netParams.popParams[tjlbl] = {'numCells': 1, 'cellType': cstr, 'cellModel': tjlbl }
    netParams.popParams[slbl]  = {'numCells': 1, 'cellType': cstr, 'cellModel': slbl  }

# import cell parameters
    tjParams = netParams.importCellParams(label=tjlbl , conds={'cellModel': tjlbl }, fileName='genrn.py' , cellName='genrn' , cellArgs=tjargs)
    sParams  = netParams.importCellParams(label=slbl  , conds={'cellModel': slbl  }, fileName='genrn.py' , cellName='genrn' , cellArgs=sargs )

# assign cell parameters
    netParams.cellParams[tjlbl] = tjParams
    netParams.cellParams[slbl]  = sParams

    stimstr = 'stim%d' %(i)

# current clamp -- around 0.5 nA
    netParams.stimSourceParams[stimstr] = {'type': 'IClamp', 'delay': cfg.delay, 'dur': 2.5, 'amp': cs(i)}
    netParams.stimTargetParams[stimstr + tjlbl] = {'source': stimstr, 'conds': {'cellModel': tjlbl }, 'sec': 'drgperi', 'loc': 0.0}
    netParams.stimTargetParams[stimstr + slbl ] = {'source': stimstr, 'conds': {'cellModel': slbl  }, 'sec': 'drgsoma', 'loc': 0.0}

# voltage clamp
'''
    netParams.stimSourceParams[stimstr] = {'type': 'VClamp', 'dur': [delay, 2.5, 2.5], 'amp': [-57, 10, -57]}    
    netParams.stimTargetParams[stimstr] = {'source': stimstr, 'conds': {'popLabel': 'cnrn'}, 'sec': 'drgsoma', 'loc': 0.5}
'''