from neuron import h
from genrn import genrn
from plot import plot_data
from copy import deepcopy as dcp
import re

h.load_file("stdrun.hoc")

h.v_init, h.celsius = -58.91, 22

numcells = 1
secs   = {'drgperi': {'nseg':257, 'L':5000,  'diam': 0.8 },
          'drgstem': {'nseg':3,   'L':75,    'diam': 1.4 },
          'drgsoma': {'nseg':1,   'L':30,    'diam': 23  },
          'drgcntr': {'nseg':363, 'L':5000,  'diam': 0.4 }}
nav17, nav18  = 'nav17h', 'nav18m'
mechs  = { nav17 : {'gnabar': 0.018 },
           nav18 : {'gnabar': 0.026 },
          'kdr'  : {'gkbar' : 0.0035},
          'ka'   : {'gkbar' : 0.0055},
          'pas'  : {'g': 5.75e-5, 'e': h.v_init}}
ions   = {'na':  67.1,
          'k' : -84.7 }
props  = {'cm': 1.2,
          'Ra': 123}
cons   = (('drgstem', 'drgperi'),
          ('drgsoma', 'drgstem'),
          ('drgcntr', 'drgperi'))
# tjargs = {'secs': secs, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': cons}
sargs  = {'secs': {'drgsoma': secs['drgsoma']}, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': ()}

csomas = {}
ctjs   = {}
vstims = {}
recvs  = {}

vars = ['gna', 'ina']
for cell in range(numcells):
# set up cells
    csomas[cell] = genrn(**sargs)
# set up stims
# VClamp as vstim
#    vstim = h.VClamp(csomas[cell].drgsoma(0.5))
#    vstim.dur[0], vcstim.dur[1], vcstim.dur[2] = 50, 50, 0
#    vstim.amp[0], vcstim.amp[1], vcstim.amp[2] = h.v_init, 0, h.v_init
# SEClamp as vstim
    vstim = h.SEClamp(csomas[cell].drgsoma(0.5))
    vstim.dur1, vstim.dur2, vstim.dur3 = 50, 50, 0
    vstim.amp1, vstim.amp2, vstim.amp3 = h.v_init, 0, h.v_init
# set up recordings
    vstims[cell] = vstim
    for ion in ions.keys():
        for mech in csomas[cell]('drgsoma').ions[ion]:
            trstr = "i%s_%s" %(ion, mech)
            trace = h.Vector()
            trace.record(getattr(csomas[cell].drgsoma(0.5), '_ref_%s' %(trstr)))
            recvs["%s:%s" %(cell, trstr)] = trace
    recvs["%s:voltage"] = h.Vector()
    recvs["%s:voltage"].record(csomas[cell].drgsoma(0.5)._ref_v)
tv = h.Vector()
tv.record(h._ref_t)

# simulate
h.dt, h.steps_per_ms, h.tstop = 0.0125, 0.5, 100
#cvode = h.CVode()
#cvode.active()
h.t = 0
h.finitialize(h.v_init)
h.stdinit()
# time vector for when parameters are changed, last value is when the sim should end
tgls = [
    [0  , {'dt': 5     , 'steps_per_ms': 0.2}, []],
    [45 , {'dt': 0.0125, 'steps_per_ms': 2  }, []],
    [55 , {'dt': 0.0125, 'steps_per_ms': 2  }, []],
    [100, {}, []]# end of simulation
]

for tgl in tgls:
    runto, attrs, execs = tgl[0], tgl[1], tgl[2]
    h.continuerun(runto)
    for attr in attrs:
        setattr(h, attr, attrs[attr])
# in case some hoc toggle function must be called.
    for exstr in execs:
        exec(exstr)
    h.setdt()

# plot traces
for trace in recvs:
    plot_data(tv, recvs[trace], [trace], 'data/', trace)
pass