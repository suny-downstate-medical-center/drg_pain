import sys
sys.path.append('..')
from netpyne import specs
try:
    from __main__ import cfg
except:
    from cfg import cfg

from cells import cableRule, somaRule, mandgeSomaRule
import numpy as np
from itertools import product

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

# playing parameters in init
# netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}
# netParams.stimSourceParams['vclamp'] = {'type': 'VClamp', 'dur': [0, 0, 0], 'amp': [0, 0, 0], 'gain': 1e5, 'rstim': 1, 'tau1': 0.1, 'tau2': 0}

somas = [somaRule, mandgeSomaRule]
axons = [cableRule]

vstims = cfg.vstims

cellRules = {}

for soma in [ somaRule ]:
    for vstim in vstims:
        cellType = {'model': "%s" %(soma['label']), 'stim': 'vc', 'val': vstim}
        cellLbl = str(cellType)
        cellRules[cellLbl] = netParams.importCellParams(label= cellLbl, conds={'cellType': cellType},
                                                        fileName= 'cells.py', cellName= 'createSoma',
                                                        cellArgs= {'somaRule': soma})
        netParams.cellParams[cellLbl] = cellRules[cellLbl]
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'VClamp', 'amp': [-70, vstim, 0], 'dur': [cfg.dur[0], cfg.dur[1] - cfg.dur[0], 0]}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'soma', 'loc': 0.5}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    pprint(cellRules)
