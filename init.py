from netpyne import sim
import numpy as np

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

def sinf(peak, duration, t):
    return peak * np.sin( t * np.pi / duration )

def rmpf(peak, duration, t):
    return peak * t / duration

def plsf(peak, duration, t):
    i = np.empty(duration)
    return i.fill(peak)

def stim(peak, duration, delay, f):
    np = np.zeros(0, delay,    cfg.dt)
    tv = np.arange(0, duration, cfg.dt)
    return np.concatenate((dv,f(peak,duration,tv)))

#netParams.stimTargetParams['iclamp->so'] = {'source': 'iclamp', 'conds': {'morpho': 'so'}, 'sec': 'soma', 'loc': 0.5}
#netParams.stimTargetParams['iclamp->tj'] = {'source': 'iclamp', 'conds': {'morpho': 'tj'}, 'sec': 'peri', 'loc': 0.0}

t = sim.h.Vector( np.arange(0, cfg.duration, cfg.dt) )

npstim = stim(30, cfg.peak, cfg.dur, rmpf)

len(t)-len(npstim)
npin = np.pad(npstim, len(t) - len(npstim))
vcin = sim.h.Vector(npstim)
for cell in sim.net.cells:
        try:
            vcstim.play(cell.stims[0]['hObj']._ref_amp, t, True)
        except:
            pass

#sim.simulate()
#sim.analyze()

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
