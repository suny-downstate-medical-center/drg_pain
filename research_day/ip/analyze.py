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

isi = {}

for cell in net['cells']:
    interval = cell['tags']['cellType']['isi']
    id = cell.gid
    wend = int(cfg.delay / cfg.recordStep)
    window = (interval * 30.5) / cfg.recordStep
    for var in ['NaV1.7']:
        trace = np.abs( sim[var]['cell_%i' %(id)])
        pulseauc = [0]
        sumauc = 0
        wstart = int(cfg.delay / cfg.recordStep)
        wend = wstart + int(interval / cfg.recordStep)
        nlauc = trace[ wstart: wend ].sum() * 0.5 * 1808.6 * 1e6 * 1e-8
        for pulse in range( 0, 30):
            sumauc += trace[ wstart: wend ].sum() * 0.5 * 1808.6 * 1e6 * 1e-8 / nlauc
            pulseauc.append(sumauc)
            wstart += int(interval / cfg.recordStep)
            wend += int(interval / cfg.recordStep)
        if interval in isi:
            isi[interval] = pulseauc
        else:
            isi[interval] = pulseauc

plt.title("NaV 1.7 normalized current")

for interval in isi:
    plt.plot(isi[interval], label="ISI/freq: %s ms/%d Hz" %(interval, np.round(1000/ interval, 0) ) )

plt.legend()
plt.xlabel("pulse #")
plt.ylabel("total normalized current")
plt.savefig("NaV17.png")

isi = {}
for cell in net['cells']:
    interval = cell['tags']['cellType']['isi']
    id = cell.gid
    wend = int(cfg.delay / cfg.recordStep)
    window = (interval * 30.5) / cfg.recordStep
    for var in ['v']:
        trace = np.array( sim[var]['cell_%i' %(id)])
        apsarr = [0]
        aps = 0
        wstart = int(cfg.delay / cfg.recordStep)
        wend = wstart + int(interval / cfg.recordStep)
        for pulse in range( 0, 30):
            aps += (trace[ wstart: wend ] > -25).sum() > 0
            apsarr.append(aps)
            wstart += int(interval / cfg.recordStep)
            wend += int(interval / cfg.recordStep)
        if interval in isi:
            isi[interval] = apsarr
        else:
            isi[interval] = apsarr

plt.title("AP response to stimulus")

for interval in isi:
    plt.plot(isi[interval], label="ISI/freq: %s ms/%d Hz" %(interval, np.round(1000/ interval, 0) ) )

plt.legend()
plt.xlabel("pulse #")
plt.ylabel("cumulative APs")
plt.savefig("APs.png")


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