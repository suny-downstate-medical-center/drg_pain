from netpyne import sim
import numpy as np

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)

def waveform(peak, duration, delay):
    np.zeros(delay/cfg.dt)



    



netParams.stimSourceParams['iclamp'] = {'type': 'IClamp', 'amp': 0.0, 'dur': 1000, 'delay': 0}
netParams.stimTargetParams['iclamp->so'] = {'source': 'iclamp', 'conds': {'morpho': 'so'}, 'sec': 'soma', 'loc': 0.5}
netParams.stimTargetParams['iclamp->tj'] = {'source': 'iclamp', 'conds': {'morpho': 'tj'}, 'sec': 'peri', 'loc': 0.0}

t = sim.h.Vector(np.arange(0, cfg.duration/(cfg.dt)))

peak
duration
npstim =
vcstim = h.Vector(npstim)
for cell in sim.net.cells:
        try:
            stim
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
