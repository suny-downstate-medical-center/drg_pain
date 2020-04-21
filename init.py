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
    'tau'      : {'rgx': re.compile('tau')  , 'xaxis': 't (ms)', 'yaxis': 'tau (1/ms)' },
    'inf'      : {'rgx': re.compile('inf')  , 'xaxis': 't (ms)', 'yaxis': 'inf (mv)'   },
    'voltage'  : {'rgx': re.compile('v_')   , 'xaxis': 't (ms)', 'yaxis': 'v (mv)'     },
    'current'  : {'rgx': re.compile('ina_') , 'xaxis': 't (ms)', 'yaxis': 'i (nA/3.14cm2)' }
}

grp0 = lambda id: id == 0
grp1 = lambda id: id != 0
# ODict, cell_# corresponds to order of creation.
xdata = data['t']
for group in traceGroups:
    grp = traceGroups[group]
    for key in cfg.recordTraces:
        # traces for specific group - [labels, ydatas]
        traces = {"vclamp": {'labels': [], 'ydatas':[], 'conds': grp0},
                  "iclamp": {'labels': [], 'ydatas':[], 'conds': grp1}}
        if grp['rgx'].search(key):
            for cell in data[key]:
                # filter out specific cells.
                id = int(cell[5:])
                for trace in traces:
                    if (data[key][cell]) and traces['conds'](id):
                        traces[trace]['labels'].append("%s:%s" %(cell, key))
                        traces[trace]['ydatas'].append(data[key][cell])
        for trace in traces:
            trc = traces[trace]
            if trc['ydatas']:
                plot_data(title="%s_%s" %(group, trace), xaxis=grp['xaxis'], yaxis=grp['yaxis'], labels=trc['labels'], xdatas=xdata, ydatas=trc['ydatas'])

# sim.analyze()