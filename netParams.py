from netpyne import specs

try:
    from __main__ import cfg
except:
    from cfg import cfg
import numpy as np

from itertools import product

simso, simtj, simxso, simxtj = cfg.simso, cfg.simtj, cfg.simxso, cfg.simxtj
mttxss, mn1p8s, mn1p9s = cfg.mttxss, cfg.mn1p8s, cfg.mn1p9s

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

params = product(mttxss, mn1p8s, mn1p9s)
# params = product( amps, durs, mn1p8s )
# netParams.synMechParams['E2S'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0}

netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 1000, 'delay': 0}

for mttxs, mn1p8, mn1p9 in params:

    # create unique tag strings for soma and tjunction
    if simso:
        solbl = 'socnrn(mn1p7:%.3fx)(mn1p8:%.3fx)(mn1p9:%.3fx)' % (mttxs, mn1p8, mn1p9)
        # soma cell model
        soRules = netParams.importCellParams(label= solbl, conds={'cellType': solbl, 'cellModel': solbl},
                                             fileName= 'cells.py', cellName= 'npSoma',
                                             cellArgs= {'mulnattxs': 1.5, 'mulnav1p8': mn1p8, 'mulnav1p9': mn1p9})
        # soRules = netParams.importCellParams(label= solbl, conds={'cellType': solbl, 'cellModel': solbl}, fileName='morphology.hoc', cellName='drg')
        print(soRules)
        netParams.cellParams[solbl] = soRules
        netParams.popParams[solbl] = {'numCells': 1, 'cellType': solbl, 'cellModel': solbl, 'morpho': 'so'}
        netParams.stimTargetParams['ic->'+solbl] = {'source': 'iclamp', 'conds': {'cellType': solbl}, 'sec': 'soma', 'loc': 0.5}

    if simtj:
        tjlbl = 'tjcnrn(mn1p7:%.3fx)(mn1p8:%.3fx)(mn1p9:%.3fx)' % (mttxs, mn1p8, mn1p9)
        # t-junction model
        tjRules = netParams.importCellParams(label=tjlbl, conds={'cellType': tjlbl, 'cellModel': tjlbl},
                                             fileName='cells.py', cellName='npTJ',
                                             cellArgs={'mulnattxs': mttxs, 'mulnav1p8': mn1p8, 'mulnav1p9': mn1p9})
        netParams.cellParams[tjlbl] = tjRules
        netParams.popParams[tjlbl] = {'numCells': 1, 'cellType': tjlbl, 'cellModel': tjlbl, 'morpho': 'tj'}
        netParams.stimTargetParams['ic->'+tjlbl] = {'source': 'iclamp', 'conds': {'cellType': tjlbl}, 'sec': 'peri', 'loc': 0.0}

    if simxso:
        xsolbl = 'xsocnrn(wtmn1p7:%.3fx)(mn1p8:%.3fx)(mn1p9:%.3fx)' % (mttxs, mn1p8, mn1p9)
        # mutant soma model
        xsoRules = netParams.importCellParams(label= mxlbl, conds={'cellType': mxlbl, 'cellModel': mxlbl},
                                              fileName= 'cells.py', cellName='npSomaMut',
                                              cellArgs= {'wtp': mttxs})
        netParams.cellParams[xsolbl] = xsoRules
        netParams.popParams[xsolbl] = {'numCells': 1, 'cellType': xsolbl, 'cellModel': xsolbl, 'morpho': 'so'}

    if simxtj:
        xtjlbl = 'xtjcnrn(wtmn1p7:%.3fx)(mn1p8:%.3fx)(mn1p9:%.3fx)' % (mttxs, mn1p8, mn1p9)
        # mutant t-junction model
        xtjRules = netParams.importCellParams(label=xtjlbl, conds={'cellType': xtjlbl, 'cellModel': xtjlbl},
                                              fileName='cells.py', cellName='npTJMut',
                                              cellArgs={'wtp': mttxs})
        netParams.cellParams[xtjlbl] = xtjRules
        netParams.popParams[xtjlbl] = {'numCells': 1, 'cellType': xtjlbl, 'cellModel': xtjlbl, 'morpho': 'tj'}


if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    pprint(soRules)
