from netpyne import specs

try:
    from __main__ import cfg
except:
    from cfg import cfg
import numpy as np

from itertools import product

simso, simtj, simxso, simxtj = cfg.simso, cfg.simtj, cfg.simxso, cfg.simxtj
freqs, npulsess, durs, amps, mttxss, mn1p8s, mn1p9s = cfg.freqs, cfg.npulsess, cfg.durs, cfg.amps, cfg.mttxss, cfg.mn1p8s, cfg.mn1p9s

# NetParams object to store network parameters
netParams = specs.NetParams()  # object of class NetParams to store the network parameters

params = product( freqs, npulsess, durs, amps, mttxss, mn1p8s, mn1p9s)
# params = product( amps, durs, mn1p8s )
# netParams.synMechParams['E2S'] = {'mod': 'Exp2Syn', 'tau1': 0.1, 'tau2': 5.0, 'e': 0}

for freq, npulses, dur, amp, mttxs, mn1p8, mn1p9 in params:
    # set up current clamp definitions, NetStim and IPClamp point process
    nslbl = 'Stim(%dHz)' % (freq)
    # pplbl = 'IPC(%.2fnAx%.1fms)' % (dur, amp)
    pplbl = 'E2S'

    netParams.stimSourceParams[nslbl] = {'type': 'NetStim', 'rate': freq, 'noise': 0, 'start': 45, 'number': npulses}
    # netParams.synMechParams[pplbl] = {'mod': 'IPClamp', 'dur': dur, 'amp': amp}

    # create unique tag strings for soma and tjunction
    if simso:
        solbl = 'socnrn(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
        # soma cell model
        soRules = netParams.importCellParams(label= solbl, conds={'cellType': solbl, 'cellModel': solbl},
                                             fileName= 'cells.py', cellName= 'npSoma',
                                             cellArgs= {'mulnattxs': mttxs, 'mulnav1p8': mn1p8, 'mulnav1p9': mn1p9})
        print(soRules)
        netParams.cellParams[solbl] = soRules
        netParams.popParams[solbl] = {'numCells': 1, 'cellType': solbl, 'cellModel': solbl}
        # soma stim
        netParams.stimTargetParams['%s->%s%s' % (nslbl, pplbl, solbl)] = {'source': nslbl, 'conds': {'pop': solbl},
                                                                          'sec': 'soma', 'loc': 0.5, 'weight': 1,
                                                                          'delay': 5, 'synMech': 'E2S'}
        #                                                                   'delay': 5, 'synMech': pplbl}

    if simtj:
        tjlbl = 'tjcnrn(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
        # t-junction model
        tjRules = netParams.importCellParams(label=tjlbl, conds={'cellType': tjlbl, 'cellModel': tjlbl},
                                             fileName='cells.py', cellName='npTJ',
                                             cellArgs={'mulnattxs': mttxs, 'mulnav1p8': mn1p8, 'mulnav1p9': mn1p9})
        netParams.cellParams[tjlbl] = tjRules
        netParams.popParams[tjlbl] = {'numCells': 1, 'cellType': tjlbl, 'cellModel': tjlbl}
        # tj stim
        netParams.stimTargetParams['%s->%s%s' % (nslbl, pplbl, tjlbl)] = {'source': nslbl, 'conds': {'pop': tjlbl},
                                                                          'sec': 'peri', 'loc': 0.0, 'weight': 1,
                                                                          'delay': 5, 'synMech': 'E2S'}
        #                                                                   'delay': 5, 'synMech': pplbl}

    if simxso:
        xsolbl = 'xsocnrn(wtn1p7:%.3f)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
        # mutant soma model
        xsoRules = netParams.importCellParams(label= mxlbl, conds={'cellType': mxlbl, 'cellModel': mxlbl},
                                              fileName= 'cells.py', cellName='npSomaMut',
                                              cellArgs= {'wtp': mttxs})
        netParams.cellParams[xsolbl] = xsoRules
        netParams.popParams[xsolbl] = {'numCells': 1, 'cellType': xsolbl, 'cellModel': xsolbl}
        # mutant soma stim
        netParams.stimTargetParams['%s->%s%s' % (nslbl, pplbl, mxlbl)] = {'source': nslbl, 'conds': {'pop': mxlbl},
                                                                          'sec': 'soma', 'loc': 0.5, 'weight': 1,
                                                                          'delay': 5, 'synMech': 'E2S'}
        #                                                                   'delay': 5, 'synMech': pplbl}

    if simxtj:
        xtjlbl = 'xtjcnrn(wtn1p7:%.3f)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
        # mutant t-junction model
        xtjRules = netParams.importCellParams(label=xtjlbl, conds={'cellType': xtjlbl, 'cellModel': xtjlbl},
                                              fileName='cells.py', cellName='npTJMut',
                                              cellArgs={'wtp': mttxs})
        netParams.cellParams[xtjlbl] = xtjRules
        netParams.popParams[xtjlbl] = {'numCells': 1, 'cellType': xtjlbl, 'cellModel': xtjlbl}
        # mutant soma stim
        netParams.stimTargetParams['%s->%s%s' % (nslbl, pplbl, xtjlbl)] = {'source': nslbl, 'conds': {'pop': xtjlbl},
                                                                           'sec': 'peri', 'loc': 0.0, 'weight': 1,
                                                                           'delay': 5, 'synMech': 'E2S'}
        #                                                                   'delay': 5, 'synMech': pplbl}

if __name__ == '__main__':
    from pprint import pprint
    # print('---TJ---')
    # pprint(tjRules)
    print('--SOMA--')
    pprint(soRules)
