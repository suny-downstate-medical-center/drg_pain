from netpyne import sim
from itertools import product
from npvec import npvec
import numpy as np
import matplotlib.pyplot as plt

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

#netParams.stimTargetParams['iclamp->so'] = {'source': 'iclamp', 'conds': {'morpho': 'so'}, 'sec': 'soma', 'loc': 0.5}
#netParams.stimTargetParams['iclamp->tj'] = {'source': 'iclamp', 'conds': {'morpho': 'tj'}, 'sec': 'peri', 'loc': 0.0}

iclampv = vec(cfg.duration, cfg.dt, 0)

base = cfg.base
peak = cfg.peak
dur = cfg.dur

base = 0
amps = np.linspace([-0.05, 0.05, 101]
delta = 0
dur  = 100
iclampv = npvec(cfg.duration, cfg.dt, base)
for amp in amps:
    iclampv.plsf(delta, 100, amp)
    delta = delta + dur

icin = sim.h.Vector(iclampv.vector)
t = sim.h.Vector(iclampv.t)

# Choi
# Membrane potential was set by constant current injection
# (−13.74 pA for −70 mV, −7.24 pA for −65 mV, 9.55 pA for −55 mV, and 25.64 pA for −50 mV)

for cell in sim.net.cells:
        try:
            icin.play(cell.stims[0]['hObj']._ref_amp, t, True)
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
