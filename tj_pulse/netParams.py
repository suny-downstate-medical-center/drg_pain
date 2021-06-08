import sys
sys.path.append('..')
from netpyne import specs
try:
    from __main__ import cfg
except:
    from cfg import cfg

from cells import cableRule, somaRule, somaRuleTD, mandgeSomaRule
from itertools import product
import copy
import numpy as np
from pprint import pprint

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

model = [cableRule, somaRuleTD]

lbl = str((model[0]['label'], model[1]['label']))

params = {}

#stim params
for isi, amp in product(cfg.isis, cfg.amps):
    cellType = {'model': "%s" % (lbl), 'isi': isi, 'amp': amp}
    cellLbl = str(cellType)
    param = netParams.importCellParams(label=lbl, conds={'cellType': cellType},
                                       fileName='cells.py', cellName='createTJ',
                                       cellArgs={'cableRule': model[0], 'somaRule': model[1]}).todict()
    netParams.cellParams[cellLbl] = param
    netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'cblperi', 'loc': 0.1}
    netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
    netParams.stimSourceParams[cellLbl] = {'type': 'IClamp', 'amp': 0, 'delay': 0, 'dur': cfg.duration}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    # for cellLbl in netParams.cellParams:
    #     pprint(netParams.cellParams[cellLbl])
