import sys
sys.path.append('../..')
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

isis = cfg.isis

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

# playing parameters in init
# netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}
# netParams.stimSourceParams['vclamp'] = {'type': 'VClamp', 'dur': [0, 0, 0], 'amp': [0, 0, 0], 'gain': 1e5, 'rstim': 1, 'tau1': 0.1, 'tau2': 0}

somas = [somaRule ]
axons = [cableRule]

params = {}
for soma in somas:
# need todict() for deepcopy()
    params[soma['label']] = netParams.importCellParams(label= soma['label'], conds={'cellType': soma['label']},
                                                       fileName= 'cells.py', cellName= 'createSoma',
                                                       cellArgs= {'somaRule': soma }).todict()

for soma in somas:
    for isi in isis:
        cellType = {'model': "%s" %(soma['label']), 'isi': isi}
        cellLbl = str(cellType)
        param = copy.deepcopy(params[soma['label']])
        param['conds']['cellType'] = cellType
        netParams.cellParams[cellLbl] = param
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'IClamp', 'amp': 0, 'delay': 0, 'dur': cfg.duration}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'soma', 'loc': 0.5}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    for cellLbl in netParams.cellParams:
        pprint(netParams.cellParams[cellLbl])
