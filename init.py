from netpyne import sim
from plot import plot_data
import re

cfg, netParams = sim.readCmdLineArgs()	
sim.create(simConfig = cfg, netParams = netParams)
sim.simulate()
"""
#MPI rank
sim.pc.barrier()
sim.gatherData()
"""
data = sim.allSimData

traceGroups = {
    'tau'      : {'rgx': re.compile('tau'), 'xaxis': 't (ms)', 'yaxis': 'tau (1/ms)' },
    'inf'      : {'rgx': re.compile('inf'), 'xaxis': 't (ms)', 'yaxis': 'inf (mv)'   },
    'voltage'  : {'rgx': re.compile('v_') , 'xaxis': 't (ms)', 'yaxis': 'v (mv)'     },
    'current'  : {'rgx': re.compile('i_') , 'xaxis': 't (ms)', 'yaxis': 'i (nA/cm2)' }
}

xdata = data['t']
for group in traceGroups:
    grp = traceGroups[group]
    for key in cfg.recordTraces:
        ydatas = []
        labels = []
        if grp['rgx'].search(key):
            ydatas.append(data[key])
            for cell in data[key]:
                ydatas.append(data[key][cell])
                labels.append("%s:%s" %(cell, key))
        if ydatas:
            plot_data(title=group, xaxis=grp['xaxis'], yaxis=grp['yaxis'], labels=labels, xdatas=xdata, ydatas=ydatas)

#sim.analyze()