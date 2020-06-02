from neuron import h
from genrn import genrn
from plot import plot_data, plot_groups
import re
# from copy import deepcopy as dcp

h.load_file("stdrun.hoc")

h.v_init, h.celsius = -58.91, 22

numcells = 10
currmax = 0.3
secs   = {'drgperi': {'nseg':257, 'L':5000,  'diam': 0.8, 'cm': 1.2, 'Ra': 123 },
          'drgstem': {'nseg':3,   'L':75,    'diam': 1.4, 'cm': 1.2, 'Ra': 123 },
          'drgsoma': {'nseg':1,   'L':30,    'diam': 23 , 'cm': 1.2, 'Ra': 123 },
          'drgcntr': {'nseg':363, 'L':5000,  'diam': 0.4, 'cm': 1.2, 'Ra': 123 }}
nav17, nav18  = 'nav17h', 'nav18m'
kdr, ka = 'kdr', 'kam'
mechs  = { nav17 : {'gnabar': 0.035 },
           nav18 : {'gnabar': 0.03 },
           kdr   : {'gkbar' : 0.0035},
#           ka    : {'gkbar' : 0.0055},
          'pas'  : {'g': 5.75e-5, 'e': h.v_init}}
ions   = {'na':  67.1,
          'k' : -84.7 }
cons   = (('drgstem', 'drgperi'),
          ('drgsoma', 'drgstem'),
          ('drgcntr', 'drgperi'))
# tjargs = {'secs': secs, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': cons}
sargs  = {'secs': {'drgsoma': secs['drgsoma']}, 'mechs': mechs, 'ions': ions, 'cons': ()}
def setVClamp(seg, durs, amps):
## VClamp as vstim
    amps = [x if isinstance(x, (int, float, complex)) else h.v_init for x in amps]
    vstim = h.VClamp(seg)
    vstim.dur[0], vstim.dur[1], vstim.dur[2] = durs[0], durs[1], durs[2]
    vstim.amp[0], vstim.amp[1], vstim.amp[2] = amps[0], amps[1], amps[2]
## SEClamp as vstim
#    vstim = h.SEClamp(csomas[cell].drgsoma(0.5))
#    vstim.dur1, vstim.dur2, vstim.dur3 = durs[0], durs[1], durs[2]
#    vstim.amp1, vstim.amp2, vstim.amp3 = amps[0], amps[1], amps[2]
    return vstim
def setIClamp(seg, delay, dur, amp):
    istim = h.IClamp(seg)
    istim.delay, istim.dur, istim.amp = delay, dur, amp
    return istim

csomas, ctjs, stims, recvs = {}, {}, {}, {"voltage": {}}

vars = ["i%s" %(i) for i in ions] + ["g%s" %(i) for i in ions]
vars = vars + ["n", "h"]
for cell in range(numcells+1):
## set up cells
    csomas[cell] = genrn(**sargs)
## set up stims
## VClamp as vstim
    if (cell == 0):
        stims[cell] = setVClamp(csomas[cell]('drgsoma')(0.5), [50, 3, 50], [-57, 10, -57])
    else:
        stims[cell] = setIClamp(csomas[cell]('drgsoma')(0.5), 50, 5, currmax * cell / numcells)
## set up recordings
    for var in vars:
        for mech in mechs:
            trstr = "%s_%s" %(var, mech)
            if hasattr(csomas[cell].drgsoma(0.5), '_ref_%s' %(trstr)):
                if trstr not in recvs:
                    recvs[trstr] = {}
                trace = h.Vector()
                trace.record(getattr(csomas[cell].drgsoma(0.5), '_ref_%s' %(trstr)))
                recvs[trstr]["cell_%s" %(cell)] = trace
                print("tracing %s for cell_%s" %(trstr, cell))
    vv = h.Vector()
    vv.record(csomas[cell].drgsoma(0.5)._ref_v)
    recvs["voltage"]["cell_%s" %(cell)] = vv
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
    [0  , {'dt': 5     , 'steps_per_ms': 0.2}, []],
    [45 , {'dt': 0.0125, 'steps_per_ms': 2  }, []],
    [55 , {'dt': 0.05, 'steps_per_ms': 2  }, []],
    [200, {}, []]# end of simulation
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
area = csomas[0]('drgsoma')(0.5).area()
re_i = re.compile('(ina)|(ik)')
for trace in recvs:
    if re_i.search(trace):
        for cell in recvs[trace]:
            recvs[trace][cell].mul(area * 1e-2)

tgs = {
    'conductivity': {'rgx': re.compile('(gna)|(gk)'), 'xaxis': 't (ms)', 'yaxis': 'g (S/cm2)', 'conds': lambda id: True},
    'current'     : {'rgx': re_i                    , 'xaxis': 't (ms)', 'yaxis': 'i (nA)'   , 'conds': lambda id: True},
    'voltage'     : {'rgx': re.compile('voltage')   , 'xaxis': 't (ms)', 'yaxis': 'v (mV)'   , 'conds': lambda id: True},
}
tcs = {
    'vclamp' : {'labels': [], 'ydatas': [], 'conds': lambda id: id == 0},
    'iclamp' : {'labels': [], 'ydatas': [], 'conds': lambda id: id != 0},
}
# plot_groups(data=recvs, keys=recvs.keys(), tracegroups=tgs, tracecells=tcs, showmins=True, showmaxs=True)
plot_groups(data=recvs, keys=recvs.keys(), tracegroups=tgs, tracecells=tcs)
## old plot traces option
# xdatas = [None, [0, h.t], [0, h.t]]
# ydatas = [None, None, None]
# labels = [None, None, None]
# colors = ['b', 'g', 'g']
# lines  = ['-', ':', ':']
#
# for trace in recvs:
#     for cell in recvs[trace]:
#         ydata = recvs[trace][cell]
#         if trace[0] == 'i':
#             ydata.mul(area * 1e-2)
#         xdatas[0] = tv
#         ydatas[0], ydatas[1], ydatas[2] = ydata, [min(ydata)]*2, [max(ydata)]*2
#         labels[0], labels[1], labels[2] = trace, "min:%f" %(ydatas[1][0]), "max:%f" %(ydatas[2][0])
#         plot_data(xdatas=xdatas, ydatas=ydatas, labels=labels, prefix='data/', title="%s_%s" %(cell, trace),
#                   xaxis='time (ms)', yaxis=trace, colors=colors, lines=lines)