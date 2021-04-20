from cells import h, genrn, somaRule, cableRule, tigerholmCableRule, choiSomaRule, mandgeSomaRule, hInit, createSoma, createCable, createTJ
from npvec import npvec
import numpy as np
from matplotlib import pyplot as plt
from itertools import product
import logging as lgg

h.load_file('stdrun.hoc')
#h.dt is 0.025

#cells

somas = {}
cables = {}
tjs = {}

#stims
iclamps = {}
vclamps = {}

#rec vars
traces = {}

for rule in [somaRule, mandgeSomaRule]:
    label = rule['label']
    soma = createSoma(rule)
    iclamp = h.IClamp(soma('soma')(0.5))
    iclamp.dur = 10000
    for loc, var in product([['soma', 0.5]], ['v', 'ina_nav1p7', 'ina_nav1p8']):
        sec, x = loc
        attr = '_ref_%s' %(var)
        if hasattr(soma(sec)(x), attr):
            trace = h.Vector()
            trace.record(getattr(soma(sec)(x), attr))
            if label not in traces:
                traces[label] = {}
            traces[label]["%s(%.1f).%s" %(sec, x, var)] = trace
        else:
            lgg.info("missing attribute: %s(%.1f).%s" %(sec, x, var))
    somas[label] = soma
    iclamps[label] = iclamp

for rule in [cableRule]:
    label = rule['label']
    cable = createCable(rule)
    iclamp = h.IClamp(cable('cable')(0.0))
    iclamp.dur = 10000
    for loc, var in product([['cable', 0.0], ['cable', 0.5], ['cable', 1.0]], ['v', 'ica', 'ik', 'ina']):
        sec, x = loc
        attr = '_ref_%s' %(var)
        if hasattr(cable(sec)(x), attr):
            trace = h.Vector()
            trace.record(getattr(cable(sec)(x), attr))
            if label not in traces:
                traces[label] = {}
            traces[label]["%s(%.1f).%s" %(sec, x, var)] = trace
        else:
            lgg.info("missing attribute: %s(%.1f).%s" %(sec, x, var))
    cables[label] = cable
    iclamps[label] = iclamp

for cRule, sRule in [ [cableRule, somaRule] ]:
    label = "%s-%s" %(cRule['label'], sRule['label'])
    tj = createTJ(cRule, sRule)
    iclamp = h.IClamp(tj('cblperi')(0.0))
    iclamp.dur = 10000
    for loc, var in product([['cblperi', 0.0], ['cblperi', 0.5], ['cblperi', 1.0], ['drgsoma', 0.5], ['cblcntr', 0.5], ['cblcntr', 1.0]], ['v', 'ica', 'ik', 'ina', 'ina_nav1p7', 'ina_nav1p8']):
        sec, x = loc
        attr = '_ref_%s' %(var)
        if hasattr(tj(sec)(x), attr):
            trace = h.Vector()
            trace.record(getattr(tj(sec)(x), attr))
            if label not in traces:
                traces[label] = {}
            traces[label]["%s(%.1f).%s" %(sec, x, var)] = trace
        else:
            lgg.info("missing attribute: %s(%.1f).%s" %(sec, x, var))
    tjs[label] = tj
    iclamps[label] = iclamp

deltas = np.arange(100, 1001, 100)
deltas = np.arange(100, 1001,  50)
stimv = {}

amps = np.zeros(3)
amps[0] = 2
amps[1] = 0.2
amps[2] = 0.15

for amp in amps:
    ipulse = npvec(10000, h.dt, 0)
    ipulse.plsf_train(deltas, 5, amp)
    stimv[amp] = h.Vector(ipulse.vector)

tv    = h.Vector(ipulse.t)

for label in ['customCable']:
    stimv[amps[0]].play(iclamps[label]._ref_amp, tv, True)

for label in ['customSoma']:
    stimv[amps[1]].play(iclamps[label]._ref_amp, tv, True)

for label in ['customCable-customSoma']:
    stimv[amps[2]].play(iclamps[label]._ref_amp, tv, True)

# run parameters
h.finitialize(-60)
h.tstop = 1000
# t = np.arange(0, h.tstop + h.dt, h.dt)
t = h.Vector()
t.record(h._ref_t)
h.run()

#           traces[label]["%s(%.1f).%s" %(sec, x, var)]
plt.plot(t, traces['customSoma']['soma(0.5).v'], label='customSoma')
plt.legend()
plt.show()

plt.plot(t, traces['customCable']['cable(0.5).v'], label='customCable')
plt.legend()
plt.show()

plt.plot(t, traces['customCable-customSoma']['cblperi(0.0).v'], label='customTJ-cblperi')
plt.legend()
plt.show()

plt.plot(t, traces['customCable-customSoma']['drgsoma(0.5).v'], label='customTJ-drgsoma')
plt.legend()
plt.show()

plt.plot(t, traces['customCable-customSoma']['cblcntr(1.0).v'], label='customTJ-cblcntr')
plt.legend()
plt.show()

# cell = tjs['tigerholm-custom:(NaVT)']
# cell('cblperi').sec.ina_nattxsT
# cell('cblperi').sec.ina_nav1p8T