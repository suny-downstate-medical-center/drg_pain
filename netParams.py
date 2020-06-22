from netpyne import specs

try:
    from __main__ import cfg
except:
    from cfg import cfg
import numpy as np

from itertools import product

freqs, npulsess, durs, amps, mttxss, mn1p8s, mn1p9s = cfg.freqs, cfg.npulsess, cfg.durs, cfg.amps, cfg.mttxss, cfg.mn1p8s, cfg.mn1p9s

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

params = product( amps, durs, mttxss)
# params = product( amps, durs, mn1p8s )

for amp, dur, mttxs in params:
# for amp, dur, mn1p8 in params:
# for amp, dur, mttxs, mn1p8 in params:
    # set up current clamp definitions, NetStim and IPClamp point process
    nslbl = 'Stim(%dHz)' % (freq)
    iplbl = 'IPC(%.2fnAx%.1fms)' % (dur, amp)
    netParams.stimSourceParams[nslbl] = {'type': 'NetStim', 'rate': freq, 'noise': 0, 'start': 15, 'number': npulses}
    netParams.synMechParams[iplbl] = {'mod': 'IPClamp', 'dur': dur, 'amp': amp}

    # create unique tag strings for soma and tjunction
    tjlbl = 'tjcnrn(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
    solbl = 'socnrn(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)

    # load cell designs
    # t-junction model
    tjRules = netParams.importCellParams(label=tjlbl, conds={'cellType': tjlbl, 'cellModel': tjlbl},
                                         fileName='cells.py', cellName='npTJ',
                                         cellArgs={'mulnattxs': mttxs, 'mulnav1p8': mn1p8, 'mulnav1p9': mn1p9})
    # soma cell model
    soRules = netParams.importCellParams(label= solbl, conds={'cellType': solbl, 'cellModel': solbl},
                                         fileName= 'cells.py', cellName= 'npSoma',
                                         cellArgs= {'mulnattxs': mttxs, 'mulnav1p8': mn1p8, 'mulnav1p9': mn1p9})

    # assign cell parameters
    netParams.cellParams[tjlbl] = tjRules
    netParams.cellParams[solbl] = soRules
    # assign cells to populations
    netParams.popParams[tjlbl] = {'numCells': 1, 'cellType': tjlbl, 'cellModel': tjlbl}
    netParams.popParams[solbl] = {'numCells': 1, 'cellType': solbl, 'cellModel': solbl}
    # attach current pulse to cells ( to socnrn->soma(0.5), tjcnrn->peri(0.0) )
    netParams.stimTargetParams['%s->%s%s' % (nslbl, iplbl, tjlbl)] = {'source': nslbl, 'conds': {'pop': tjlbl},
                                                                      'sec': 'peri', 'loc': 0.0, 'weight': 1,
                                                                      'delay': 5, 'synMech': iplbl}
    netParams.stimTargetParams['%s->%s%s' % (nslbl, iplbl, solbl)] = {'source': nslbl, 'conds': {'pop': solbl},
                                                                      'sec': 'soma', 'loc': 0.5, 'weight': 1,
                                                                      'delay': 5, 'synMech': iplbl}

if __name__ == '__main__':
    from pprint import pprint
    print('---TJ---')
    pprint(tjRules)
    print('--SOMA--')
    pprint(soRules)
