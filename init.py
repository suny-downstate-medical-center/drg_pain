from netpyne import sim
from itertools import product
from npvec import npvec
import numpy as np
import matplotlib.pyplot as plt

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

#netParams.stimTargetParams['iclamp->so'] = {'source': 'iclamp', 'conds': {'morpho': 'so'}, 'sec': 'soma', 'loc': 0.5}
#netParams.stimTargetParams['iclamp->tj'] = {'source': 'iclamp', 'conds': {'morpho': 'tj'}, 'sec': 'peri', 'loc': 0.0}

iclampv = npvec(cfg.duration, cfg.dt, 0)

base = cfg.base
peak = cfg.peak
dur = cfg.dur

base = -0.05
steps = 5
amps = np.linspace( 0.005, 0.025, steps)
dur = cfg.duration / 2 / steps
delta = dur
iclampv = npvec(cfg.duration, cfg.dt, base)
for amp in amps:
    iclampv.plsf(delta, dur, amp)
    delta = delta + (dur * 2)

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

plt.plot(sim.allSimData['t'], sim.allSimData['v']['cell_0'])
plt.title("Membrane Potential")
plt.xlabel("time (ms)")
plt.ylabel("voltage (mV)")
plt.show()

plt.title("Current Stimulus")
plt.xlabel("time (ms)")
plt.ylabel("current mA/cm2")
plt.plot(t, icin)
plt.show()

plt.title("NaV 1.7 / NaV 1.8 Current")
plt.plot(sim.allSimData['t'], sim.allSimData['NaV1.7']['cell_0'], color='r', label='NaV 1.7')
plt.plot(sim.allSimData['t'], sim.allSimData['NaV1.8']['cell_0'], color='b', label='NaV 1.8')
plt.legend()
plt.xlabel("time (ms)")
plt.ylabel("current mA/cm2")
plt.show()

fig = plt.figure()
fig.suptitle('NaV1.7 / NaV1.8 Current')
gs = fig.add_gridspec(2, 1, hspace=0, wspace=0)
ax0 = fig.add_subplot(gs[0,0])
ax1 = fig.add_subplot(gs[1,0])
ax0.plot(sim.allSimData['t'], sim.allSimData['NaV1.7']['cell_0'], color='r', label='NaV 1.7')
ax0.legend()
ax1.plot(sim.allSimData['t'], sim.allSimData['NaV1.8']['cell_0'], color='b', label='NaV 1.8')
ax1.legend()
plt.xlabel("time (ms)")
plt.ylabel("current mA/cm2")
plt.show()

plt.title("NaV 1.7 / NaV 1.8 Current")
plt.plot(sim.allSimData['t'], sim.allSimData['NaV1.7']['cell_0'], color='r', label='NaV 1.7')
plt.plot(sim.allSimData['t'], sim.allSimData['NaV1.8']['cell_0'], color='b', label='NaV 1.8')
plt.legend()
plt.xlabel("time (ms)")
plt.ylabel("current mA/cm2")
plt.show()

plt.title("Ion Current")
plt.plot(sim.allSimData['t'], sim.allSimData['i_pas']['cell_0'], label='i_pas')
plt.plot(sim.allSimData['t'], sim.allSimData['ina']['cell_0'], label='Na')
plt.plot(sim.allSimData['t'], sim.allSimData['ik' ]['cell_0'], label='K' )
plt.plot(sim.allSimData['t'], sim.allSimData['ica']['cell_0'], label='Ca')
plt.plot(sim.allSimData['t'], sim.allSimData['icl']['cell_0'], label='Cl')
plt.legend()
plt.xlabel("time (ms)")
plt.ylabel("current mA/cm2")
plt.show()
