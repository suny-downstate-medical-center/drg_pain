from neuron import h
from genrn import genrn
from plot import plot_groups
from cells import hGlobals, scr
import re
# from copy import deepcopy as dcp

# initialization calls
h.load_file("stdrun.hoc")
h.load_file("tautables.hoc")
for var in hGlobals:
    execstr = 'h.%s = %s' % (var, hGlobals[var])
    print('exec: %s' % (execstr))
    exec(execstr)

# cell parameters from Mandge 2018
somaCellArgs= {
    'h'    : h,
    'secs' : {'soma': scr['geom']},
    'mechs': scr['mechs'],
    'ions' : scr['ions'],
    'cons' : ()
}

# cell stimulate functions, VClamp, SEClamp and IClamp
def setVClamp(seg, durs, amps):
## VClamp as vstim
    amps = [x if isinstance(x, (int, float)) else h.v_init for x in amps]
    vstim = h.VClamp(seg)
    vstim.dur[0], vstim.dur[1], vstim.dur[2] = durs[0], durs[1], durs[2]
    vstim.amp[0], vstim.amp[1], vstim.amp[2] = amps[0], amps[1], amps[2]
    return vstim

def setSEClamp():
# SEClamp as vstim
    vstim = h.SEClamp(csomas[cell].drgsoma(0.5))
    vstim.dur1, vstim.dur2, vstim.dur3 = durs[0], durs[1], durs[2]
    vstim.amp1, vstim.amp2, vstim.amp3 = amps[0], amps[1], amps[2]
    return vstim

def setIClamp(seg, delay, dur, amp):
    istim = h.IClamp(seg)
    istim.delay, istim.dur, istim.amp = delay, dur, amp
    return istim

def setIPClamp(seg, delay, freq, number, dur, amp):
    ns = h.NetStim()
    ns.start, ns.interval, ns.number = delay, 1000/freq, number
    ipstim = h.IPClamp(seg)
    ipstim.dur, ipstim.amp = dur, amp
    nc = h.NetCon(ns, ipstim, 0, 0.5, 1)
    return [ns, nc, ipstim]

# simulation parameters
numcells = 10
currmax = 0.3

# simulation storage objects
csomas, ctjs, stims, recvs = {}, {}, {}, {"voltage": {}}

# generate record traces
trstrs = ['v',
          'ina', 'ik', 'icl', 'ica',
          'ina_nattxs', 'ina_nav1p8', 'ina_nav1p9']

for cell in range(numcells+1):
## set up cells
    csomas[cell] = genrn(**somaCellArgs)
## set up stims
## VClamp as vstim
    if (cell == 0):
        stims[cell] = setVClamp(csomas[cell].soma(0.5), [25, 3, 50], [h.v_init, 10, h.v_init])
    else:
#                                seg, delay, freq, number, dur, amp
        stims[cell] = setIPClamp(csomas[cell].soma(0.5), 25, 50, 10, 5, currmax * cell / numcells)
#        stims[cell] = setIClamp(csomas[cell].soma(0.5), 50, 5, currmax * cell / numcells)
## set up recordings
    for trstr in trstrs:
        if trstr not in recvs:
            recvs[trstr] = {}
        trace= h.Vector()
        trace.record(getattr(csomas[cell].soma(0.5), '_ref_%s' % (trstr)))
        recvs[trstr]["cell_%s" % (cell)] = trace
        print("tracing %s for cell_%s" % (trstr, cell))

# simulation script
tv = h.Vector()
tv.record(h._ref_t)
recvs['t'] = tv

## simulate
h.dt, h.steps_per_ms, h.tstop = 0.0125, 0.5, 100
# cvode = h.CVode()
# cvode.active()
h.t = 0
h.finitialize(h.v_init)
h.stdinit()

## time vector for when parameters are changed, last value is when the sim should end
tgls = [
    [0   , {'dt': 5     , 'steps_per_ms': 0.2}, []],
    [20  , {'dt': 0.0125, 'steps_per_ms': 2  }, []],
    [200 , {}, []]# end of simulation
]

for tgl in tgls:
    runto, attrs, execs = tgl[0], tgl[1], tgl[2]
    h.continuerun(runto)
    for attr in attrs:
        setattr(h, attr, attrs[attr])
## in case some hoc toggle function must be called.
    for exstr in execs:
        exec(exstr)
    h.setdt()

## additional calculations - surface area at our recording (current density * surface area = current)
## mA/cm2 * um2 * (cm2 / (1e8 * um2)) * ((1e6 * nA) / mA)
## mA * um2 * cm2 * 1e6nA
## ----------------------
##   cm2 * 1e8um2 * mA

## compute current from current density
area = csomas[0]('soma')(0.5).area()
re_i = re.compile('(ina)|(ik)|(icl)|(ica)')
for trace in recvs:
    if re_i.search(trace):
        for cell in recvs[trace]:
            recvs[trace][cell].mul(area * 1e-2)

tgs = {
    'current'     : {'rgx': re_i           , 'xaxis': 't (ms)', 'yaxis': 'i (nA)'   , 'conds': lambda id: True},
    'voltage'     : {'rgx': re.compile(r'^v'), 'xaxis': 't (ms)', 'yaxis': 'v (mV)'   , 'conds': lambda id: True},
}
tcs = {
    'vclamp' : {'labels': [], 'ydatas': [], 'conds': lambda id: id == 0},
    'iclamp' : {'labels': [], 'ydatas': [], 'conds': lambda id: id != 0},
}
# plot_groups(data=recvs, keys=recvs.keys(), tracegroups=tgs, tracecells=tcs, showmins=True, showmaxs=True)

plot_groups(data=recvs, keys=recvs.keys(), tracegroups=tgs, tracecells=tcs)
