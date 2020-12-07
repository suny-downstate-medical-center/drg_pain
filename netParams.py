from netpyne import specs

try:
    from __main__ import cfg
except:
    from cfg import cfg
import numpy as np

from itertools import product
# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

# playing parameters in init
netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}

v_inits = np.linspace( -80, -40, 21)
stims = np.linspace( 0, 0.5, 21)
for v_init in v_inits:
    for stim in stims:
        # create unique tag strings for soma and tjunction
        cellType = { 'rmp': v_init, 'stim': stim }
        cellLbl = str(cellType)
        cellRules = netParams.importCellParams(label= cellLbl, conds={'cellType': cellType},
                                               fileName= 'cells.py', cellName= 'npSoma',
                                               cellArgs= {'v_init': v_init})
        print(cellRules)
        netParams.cellParams[cellLbl] = cellRules
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimTargetParams['ic->'+cellLbl] = {'source': 'iclamp', 'conds': {'cellType': cellType}, 'sec': 'soma', 'loc': 0.5}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    pprint(cellRules)
