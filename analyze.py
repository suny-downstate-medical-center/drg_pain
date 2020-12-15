import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
from cfg import cfg
fptr = "%s/%s.pkl" %(cfg.saveFolder, cfg.simLabel)
fptr = open("data/sim.pkl", "rb")
pkld = pkl.load(fptr)
fptr.close()
net = pkld['net']
sim = pkld['simData']

voltage = {}
current = {}

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val']
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'i':
            spikes = 0
            for spkid in sim['spkid']:
                if id == spkid:
                    spikes = spikes + 1
            model = cell['tags']['cellType']['model']
            if model in current:
                current[model].append([ stim, spikes ])
            else:
                current[model] = [[ stim, spikes ]]
    except:
        pass

plt.title("# spikes")
for model in current:
    x, y = zip(*current[model])
    plt.plot( x, y, label=model)
plt.legend()
plt.xlabel("current")
plt.ylabel("# spikes")
plt.show()

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 60
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.7']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.7' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 60
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.8']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.8' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val'] - 60
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.8T']['cell_%i' %(id)] )
            peak = trace.min()
            model = "%s:%s" %( cell['tags']['cellType']['model'], 'NaV1.8T' )
            if model in voltage:
                voltage[model].append([ stim, peak ])
            else:
                voltage[model] = [[ stim, peak ]]
    except:
        pass

plt.title("NaV peak current")
for model in voltage:
    x , y = zip(*voltage[model])
    plt.plot( x, y, label=model)
plt.legend()
plt.xlabel("voltage clamp (mV)")
plt.ylabel("peak current (mA/cm2)")
plt.show()

del(net)
del(sim)
