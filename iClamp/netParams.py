import sys
sys.path.append('..')
from netpyne import specs
try:
    from __main__ import cfg
except:
    from cfg import cfg

from cells import cableRule, somaRule, mandgeSomaRule
from itertools import product
import copy
import numpy as np
from pprint import pprint

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

# playing parameters in init
# netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}
# netParams.stimSourceParams['vclamp'] = {'type': 'VClamp', 'dur': [0, 0, 0], 'amp': [0, 0, 0], 'gain': 1e5, 'rstim': 1, 'tau1': 0.1, 'tau2': 0}

somas = [somaRule]
axons = [cableRule]

istims = cfg.istims

paramsd = {}
for soma in somas:
# need todict() for deepcopy()
    cellParams = netParams.importCellParams(label= soma['label'], conds={'cellType': soma['label']},
                                            fileName= 'cells.py', cellName= 'createSoma',
                                            cellArgs= {'somaRule': soma }).todict()
    paramsd[soma['label']] = cellParams

for soma in somas:
    for istim in istims:
        cellType = {'model': "%s" %(soma['label']), 'stim': 'ic', 'val': istim}
        cellLbl = str(cellType)
        pprint(paramsd[soma['label']])
        param = copy.deepcopy(paramsd[soma['label']])
        param['conds']['cellType'] = cellType
        netParams.cellParams[cellLbl] = param
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'IClamp', 'amp': istim, 'delay': cfg.dur[0], 'dur': cfg.dur[1]}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'soma', 'loc': 0.5}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    for cellLbl in netParams.cellParams:
        pprint(netParams.cellParams[cellLbl]['conds']['cellType'])
