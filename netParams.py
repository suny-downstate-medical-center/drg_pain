from netpyne import specs
try:
    from __main__ import cfg
except:
    from cfg import cfg

from cells import somaRule, choiSomaRule, mandgeSomaRule, tigerholmCableRule
import numpy as np
from itertools import product

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

# playing parameters in init
# netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}
# netParams.stimSourceParams['vclamp'] = {'type': 'VClamp', 'dur': [0, 0, 0], 'amp': [0, 0, 0], 'gain': 1e5, 'rstim': 1, 'tau1': 0.1, 'tau2': 0}

somas = [somaRule, choiSomaRule, mandgeSomaRule]
axons = [tigerholmCableRule]

istims = cfg.istims
vstims = cfg.vstims
isis  = cfg.isis

cellRules = {}

for soma in [somaRule, choiSomaRule, mandgeSomaRule]:
    for stim in istims:
        cellType = {'model': soma['label'], 'stim': 'i', 'val': stim}
        cellLbl = str(cellType)
        cellRules[cellLbl] = netParams.importCellParams(label= cellLbl, conds={'cellType': cellType},
                                               fileName= 'cells.py', cellName= 'createSoma',
                                               cellArgs= {'cellRule': soma})
        netParams.cellParams[cellLbl] = cellRules[cellLbl]
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'IClamp', 'amp': stim, 'dur': cfg.dur[1], 'delay': cfg.dur[0]}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'soma', 'loc': 0.5}

for soma in [somaRule, choiSomaRule, mandgeSomaRule]:
    for stim in vstims:
        cellType = {'model': soma['label'], 'stim': 'v', 'val': stim}
        cellLbl = str(cellType)
        cellRules[cellLbl] = netParams.importCellParams(label= cellLbl, conds={'cellType': cellType},
                                               fileName= 'cells.py', cellName= 'createSoma',
                                               cellArgs= {'cellRule': soma})
        netParams.cellParams[cellLbl] = cellRules[cellLbl]
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'VClamp', 'dur': [cfg.dur[0], cfg.dur[1], 0], 'amp': [-60, -60+stim , 0], 'gain': 1e5, 'rstim': 1, 'tau1': 0.1, 'tau2': 0}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'soma', 'loc': 0.5}

"""
for cable in [tigerholmCableRule]:
    for isi in isis:
        cellType = {'model': cable['label'], 'stim': 'pls', 'val': isi}
        cellLbl = str(cellType)
        cellRules[cellLbl] = netParams.importCellParams(label= cellLbl, conds={'cellType': cellType},
                                               fileName= 'cells.py', cellName= 'createCable',
                                               cellArgs= {'cellRule': cable})
        netParams.cellParams[cellLbl] = cellRules[cellLbl]
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'peri', 'loc': 0.0}
"""


if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    pprint(cellRules)
