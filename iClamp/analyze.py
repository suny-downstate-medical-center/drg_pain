import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from cfg import cfg
fptr = "%s/%s.pkl" %(cfg.saveFolder, cfg.simLabel)
fptr = open("data/sim.pkl", "rb")
pkld = pkl.load(fptr)
fptr.close()
net = pkld['net']
sim = pkld['simData']

voltage = {}

for cell in net['cells']:
    stim = cell['tags']['cellType']['val']
    id = cell.gid
    for var in ['NaV1.7', 'NaV1.8', 'KA', 'KDR']:
        trace = np.abs( sim[var]['cell_%i' %(id)] )
        peak = trace.max()
        print("%s: %s mV -> %s mA/cm2" %( var, stim, peak ))
        rec = "%s:%s" %( cell['tags']['cellType']['model'], var )
        if rec in voltage:
            voltage[rec].append([ stim, peak ])
        else:
            voltage[rec] = [[ stim, peak ]]

for cell in net['cells']:
    stim = cell['tags']['cellType']['val']
    id = cell.gid
    for var in ['v']:
        trace = np.array( sim[var]['cell_%i' %(id)] )
        peak = trace.max()
        trough = trace.min()
        print("%s: %s nA -> (%s, %s) mv, " %( var, stim, peak, trough ))
        rec = "%s:%s" %( cell['tags']['cellType']['model'], var )
        if rec in voltage:
            voltage[rec].append([ stim, peak ])
        else:
            voltage[rec] = [[ stim, peak ]]

for rec in voltage:
    plt.title("NaV peak current")
    x , y = zip(*voltage[rec])
    peak = np.array( y )
    print(rec)
    maxv = peak.max()
    i = np.where(peak == maxv)[0][0]
    print("peak = %s mA/cm2 @ %s mV" %(maxv, x[i]) )
    plt.plot( x, y, label=rec)
    plt.legend()
    plt.xlabel("voltage clamp (mV)")
    plt.ylabel("peak current (mA/cm2)")
    plt.show()

#del(net)
#del(sim)

# customSoma:NaV1.7
# peak = -0.4314103303283789 mA/cm2 @ 0 mV
# customSoma:NaV1.8
# peak = -0.8159115380131626 mA/cm2 @ 10 mV


# NaV 1.7 -> 15 nA    -> 15 e-6         -> 0.692201199815413 mA/cm2
# NaV 1.8 -> 25 nA    -> 25 e-6         -> 0.9552923194497517 mA/cm2
# Area    -> 2167 um2 -> 2.167 e-5 cm2

# KA: 0 mV -> 0.040422101753871495 mA/cm2
# KDR: 0 mV -> 0.2420360846395829 mA/cm2

# KA -> 1 nA @ 0 mV -> 0.046146746654360866
# KDR -> 6 nA @ 0 mV ->  0.2768804799261652