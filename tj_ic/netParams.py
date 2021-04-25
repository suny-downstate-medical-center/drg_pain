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

# playing parameters in init
# netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 0, 'delay': 0}
# netParams.stimSourceParams['vclamp'] = {'type': 'VClamp', 'dur': [0, 0, 0], 'amp': [0, 0, 0], 'gain': 1e5, 'rstim': 1, 'tau1': 0.1, 'tau2': 0}

somas  = [somaRuleTD ]
cables = [cableRule]
tjs    = [ [cableRule, somaRuleTD] ]

params = {}
delay = cfg.delay

for tj in tjs:
    for isi, amp, mul, mut, ashft, ishft in product(cfg.isis, cfg.amps, cfg.muls, cfg.muts, cfg.ashfts, cfg.ishfts):
        tjLbl = str((tj[0]['label'], tj[1]['label']))
        cellType = {'model': "%s" % (tjLbl), 'isi': isi, 'amp': amp, 'mul': mul, 'mut': mut}
        cellLbl = str(cellType)
        # param = copy.deepcopy(params[tjLbl])
        param = netParams.importCellParams(label=tjLbl, conds={'cellType': tjLbl},
                                           fileName='cells.py', cellName='createTJ',
                                           cellArgs={'cableRule': tj[0], 'somaRule': tj[1],
                                                     'm1p7': mul, 'mut': mut,
                                                     'ashft': ashft, 'ishft': ishft,
                                                     'mk': 2, 'mkca': 1.0, 'mkm': 1.0}).todict()
        param['conds']['cellType'] = cellType
        netParams.cellParams[cellLbl] = param
        netParams.popParams[cellLbl] = {'numCells': 1, 'cellType': cellType}
        netParams.stimSourceParams[cellLbl] = {'type': 'IClamp', 'amp': amp, 'delay': delay, 'dur': cfg.duration - delay}
        netParams.stimTargetParams[cellLbl] = {'source': cellLbl, 'conds': {'cellType': cellType}, 'sec': 'cblperi', 'loc': 0.1}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    # for cellLbl in netParams.cellParams:
    #     pprint(netParams.cellParams[cellLbl])
