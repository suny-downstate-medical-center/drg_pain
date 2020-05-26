from netpyne import specs
try: 
    from __main__ import cfg
except:
    from cfg import cfg
from cellcopy import dcp, cell_copy
freq, npulses, dur, amp, mttxs, mn1p8 = cfg.freq, cfg.npulses, cfg.dur, cfg.amp, cfg.mttxs, cfg.mn1p8

# NetParams object to store network parameters
netParams= specs.NetParams()   # object of class NetParams to store the network parameters

# set up current clamp definitions, NetStim and IPClamp point process
nslbl = 'Stim(%dHz)' %(freq)
iplbl = 'IPC(%.1fnAx%.1fms)' %(dur, amp)
netParams.stimSourceParams[nslbl] = {'type': 'NetStim', 'rate': freq, 'noise': 0, 'start': 15, 'number': npulses}
netParams.synMechParams[iplbl] = {'mod': 'IPClamp', 'dur': dur, 'amp': amp}
# create unique tag strings for soma and tjunction
tjlbl= 'tjcnrn'
solbl= 'socnrn'

# load cell designs
tjRules= netParams.importCellParams(label= tjlbl, conds={'cellType': tjlbl, 'cellModel': tjlbl}, fileName= 'cells.py', cellName= 'npTJ'  , cellArgs= {'mulnattxs': mttxs, 'mulnav1p8': mn1p8})
soRules= netParams.importCellParams(label= solbl, conds={'cellType': solbl, 'cellModel': solbl}, fileName= 'cells.py', cellName= 'npSoma', cellArgs= {'mulnattxs': mttxs, 'mulnav1p8': mn1p8})

# assign cell parameters
netParams.cellParams[tjlbl]= tjRules
netParams.cellParams[solbl]= soRules
# assign cells to populations
netParams.popParams[tjlbl]= {'numCells': 1, 'cellType': tjlbl, 'cellModel': tjlbl}
netParams.popParams[solbl]= {'numCells': 1, 'cellType': solbl, 'cellModel': solbl}
# attach current pulse to cells ( to socnrn->soma(0.5), tjcnrn->peri(0.0) )
netParams.stimTargetParams['%s->%s%s' %(nslbl, iplbl, solbl)] = {'source': nslbl, 'conds': {'pop': solbl}, 'sec': 'soma', 'loc': 0.5, 'weight': 1, 'delay': 5, 'synMech': iplbl}
netParams.stimTargetParams['%s->%s%s' %(nslbl, iplbl, tjlbl)] = {'source': nslbl, 'conds': {'pop': tjlbl}, 'sec': 'peri', 'loc': 0.0, 'weight': 1, 'delay': 5, 'synMech': iplbl}

if __name__=='__main__':
    from pprint import pprint
    print('--SOMA--')
    pprint(soRules)
    print('---TJ---')
    pprint(tjRules)
