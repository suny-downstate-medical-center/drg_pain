from netpyne import sim
from itertools import product
import numpy as np
import matplotlib.pyplot as plt
cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

def sinf(peak, duration, t):
    return peak * np.sin( t * np.pi / duration )

def rmpf(peak, duration, t):
    return peak * t / duration

def plsf(peak, duration, t):
    i = np.empty( int(duration / cfg.dt) )
    i.fill(peak)
    return i

def stim(delay, duration, peak, f):
    deltv = np.zeros( int(delay / cfg.dt) )
    stmtv = np.arange(0, duration, cfg.dt)
    return di, np.concatenate((deltv,f(peak,duration,stmtv)))

#netParams.stimTargetParams['iclamp->so'] = {'source': 'iclamp', 'conds': {'morpho': 'so'}, 'sec': 'soma', 'loc': 0.5}
#netParams.stimTargetParams['iclamp->tj'] = {'source': 'iclamp', 'conds': {'morpho': 'tj'}, 'sec': 'peri', 'loc': 0.0}

t = sim.h.Vector( np.arange(0, cfg.duration, cfg.dt) )
base = cfg.base
peak = cfg.peak
dur = cfg.dur

base = 0
peak = 0.800
dur  = 300

base = 0
currvc = np.full( cfg.duration/cfg.dt, base) 
currix = 0
npstimv = 
npstim = stim(peak, dur, 100 , plsf)

npin = np.pad(npstim, (0, len(t) - len(npstim)))
vcin = sim.h.Vector(npin)

for cell in sim.net.cells:
        try:
            vcin.play(cell.stims[0]['hObj']._ref_amp, t, True)
        except:
            pass


sim.simulate()
sim.analyze()

plt.plot(sim.allSimData['t'], sim.allSimData['soma']['cell_0'])
plt.title('Voltage')
plt.show()
plt.plot(t, npin)
plt.show()

fig = plt.figure()
fig.suptitle('NaV1.7 / NaV1.8 current')
gs = fig.add_gridspec(2, 1, hspace=0, wspace=0)
ax0 = fig.add_subplot(gs[0,0])
ax1 = fig.add_subplot(gs[1,0])
ax0.plot(sim.allSimData['t'], sim.allSimData['NaV1.7']['cell_0'])
ax1.plot(sim.allSimData['t'], sim.allSimData['NaV1.8']['cell_0'])
plt.show()
"""
sim.simulate()
sim.analyze()

# Create network and run simulation
sim.create(netParams = netParams, simConfig = simConfig)
...
netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 1000, 'delay': 0}
netParams.stimTargetParams['iclamp->PYR'] = {'source': 'iclamp', 'conds': {'pop': 'S'}, 'sec': 'soma', 'loc': 0.5}
...
init_amp = 0.0
peak_amp = 0.24
ramp_up = np.linspace(init_amp, peak_amp, simConfig.duration/(simConfig.dt))
t = h.Vector(np.arange(0,simConfig.duration, simConfig.dt))
amp = h.Vector(ramp_up)
for cell in sim.net.cells:
    try:
        amp.play(cell.stims[0]['hObj']._ref_amp, t, True)
    except:
        pass
sim.simulate()
sim.analyze()
"""
