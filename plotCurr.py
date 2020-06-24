from data import DataHandler
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from itertools import product

from cfg import freqs, npulsess, amps, durs, mttxss, mn1p8s, mn1p9s

# label
# '<celltype>(mn1p7:%.3fx)(mn1p8:%.3fx)(%.3fnAx%.3fms)(%.3fHz)' % (mttxs, mn1p8, amp, dur, freq)
dh = DataHandler()
dh('data/curr.json', 'curr')

for label, chan in [ ['NaV1.7', 'nattxs'], ['NaV1.8', 'nav1p8'] ]:
    cfg.recordTraces[label] = {'sec': 'soma', 'loc': 0.5, 'var': 'ina_%s' %(chan)}
ixsren1p7 = '(.....)nAx(.....)ms.*ina_NaV1.7'
ixsren1p8 = '(.....)nAx(.....)ms.*ina_NaV1.8'

n1p7 = dh.return_arr(ixsren1p7, lambda x: x)
n1p8 = dh.return_arr(ixsren1p8, lambda x: x)

def create_surface(muls, amps):
    surface = np.zeros( (len(amps), len(muls)) )
    for i, mul in enumerate(muls):
        for j, amp in enumerate(amps):
            surface[j][i] = data[mul][amp]['val']
    return surface

mmuls, mamps = np.meshgrid(muls, amps)

fig = plt.figure()
ax  = fig.gca(projection='3d')
v_soma = create_surface(muls, amps)
ax.plot_surface(mmuls, mamps, v_soma, label='v_soma', cmap=cm.coolwarm)
ax.set_xlim(muls.max(), muls.min())
ax.set_ylim(amps.min(), amps.max())
ax.set_xlabel('NaV1.8')
ax.set_ylabel('nA')
plt.show()

