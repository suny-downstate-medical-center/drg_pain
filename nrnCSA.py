from genrn import genrn, h
from neuron import h
from copy import deepcopy as dcp
import re

h.load_file("stdrun.hoc")
h.dt, h.steps_per_ms, h.v_init, h.celsius = 0.0125, 0.5, -58.91, 22
numcells = 1
secs   = {'drgperi': {'nseg':257, 'L':5000,  'diam': 0.8 },
          'drgstem': {'nseg':3,   'L':75,    'diam': 1.4 },
          'drgsoma': {'nseg':1,   'L':30,    'diam': 23  },
          'drgcntr': {'nseg':363, 'L':5000,  'diam': 0.4 }}
nav17, nav18  = 'nav17m', 'nav18m'
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
#tjargs = {'secs': secs, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': cons}
sargs  = {'secs': {'drgsoma': secs['drgsoma']}, 'props': props, 'mechs': mechs, 'ions': ions, 'cons': ()}

csomas = {}
ctjs   = {}
recvs  = {}

vars = ['gna', 'ina']
for cell in range(numcells):
    csomas[cell] = genrn(**sargs)
    for ion in ions.keys():
        for mech in csomas[cell]('drgsoma').ions[ion]:
            trstr = "i%s_%s" %(ion, mech)
            trace = h.Vector()
            trace.record(getattr(csomas[cell].drgsoma(0.5), '_ref_%s' %(trstr)))
            recvs[trstr] = trace

recvs['t'] = h.Vector()
recvs['t'].record(h._ref_t)


