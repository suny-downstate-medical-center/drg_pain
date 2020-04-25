from netpyne import sim
from plot import plot_data, plot_groups
import re

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)
sim.simulate()
"""
#MPI rank
sim.pc.barrier()
sim.gatherData()
"""

tracegroups = {
#    'tau'         : {'rgx': re.compile('tau')       , 'xaxis': 't (ms)', 'yaxis': 'tau (1/ms)' , 'conds': lambda id: id != 0},
#    'inf'         : {'rgx': re.compile('inf')       , 'xaxis': 't (ms)', 'yaxis': 'inf (mv)'   , 'conds': lambda id: id != 0},
#    'voltage'     : {'rgx': re.compile('v_')        , 'xaxis': 't (ms)', 'yaxis': 'v (mv)'     , 'conds': lambda id: id != 0},
#    'current'     : {'rgx': re.compile('(NaV)|K')   , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' , 'conds': lambda id: id != 0},
#    'current(Na)' : {'rgx': re.compile('NaV')       , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' , 'conds': lambda id: id != 0},
#    'current(K)'  : {'rgx': re.compile('K')         , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' , 'conds': lambda id: id != 0},
    'current(Na)' : {'rgx': re.compile('NaV')       , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' , 'conds': lambda id: id == 0},
}

tracecells = {
    "vclamp": {'labels': [], 'ydatas': [], 'conds': lambda id: id == 0},
#    "iclamp": {'labels': [], 'ydatas': [], 'conds': lambda id: id != 0},
}

plot_groups(sim.allSimData, cfg.recordTraces.keys(), tracegroups, tracecells)

pass
# sim.analyze()