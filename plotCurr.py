from data import DataHandler
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product
from plot import plot_data, plot_groups
from cfg import cfg

freqs, npulses, amps, durs, mttxss, mn1p8s, mn1p9s = cfg.freqs, cfg.npulsess, cfg.amps, cfg.durs, cfg.mttxss, cfg.mn1p8s, cfg.mn1p9s

# label
# '<celltype>(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
dh = DataHandler()
dh('data/curr.json', 'curr')

#for label, chan in [ ['NaV1.7', 'nattxs'], ['NaV1.8', 'nav1p8'] ]:
#    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}
ixsren1p7 = '\(([0-9.]*)nAx([0-9.]*)ms.*NaV1.7'
ixsren1p8 = '\(([0-9.]*)nAx([0-9.]*)ms.*NaV1.8'

n1p7 = dh.return_arr(ixsren1p7, lambda x: x)
n1p8 = dh.return_arr(ixsren1p8, lambda x: x)
t = np.array(dh.data['curr_t'][0:120])

def create_trace(amp, dur):
    cn1p7 = n1p7[amp][dur]['val'][60:180]
    cn1p8 = n1p8[amp][dur]['val'][60:180]
    return cn1p7 / (cn1p7 + cn1p8)

def create_surface(dur):
    surface = []
    for amp in amps:
        surface.append(create_trace(amp, dur))
    surface = np.array(surface)
    return surface

mamps, mt = np.meshgrid(t, amps)

fig = plt.figure()
ax  = fig.gca(projection='3d')
v_soma = create_surface(15)
ax.plot_surface(mamps, mt, v_soma, label='v_soma', cmap=cm.coolwarm)
ax.set_xlim(t.min(), t.max())
ax.set_ylim(amps.min(), amps.max())
ax.set_xlabel('t')
ax.set_ylabel('amp')
plt.show()
