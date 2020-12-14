import pickle as pkl
import numpy as np
import matplotlib.pyplot as plt
import cfg
fptr = "%s/%s.pkl" %(cfg.saveFolder, cfg.)
fptr = open("data/simtest.pkl", "rb")
pkld = pkl.load(fptr)
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
            if cell['tags']['cellType']['model'] in current:
                current['model'].append([ stim, spikes ])
            else:
                current['model'] = [ stim, spikes ]
    except:
        pass

for cell in net['cells']:
    try:
        stim = cell['tags']['cellType']['val']
        id = cell.gid
        if cell['tags']['cellType']['stim'] == 'v':
            trace = np.array( sim['NaV1.7']['cell_%i' %(id)] )
            peak = trace.max()
            if cell['tags']['cellType']['model'] in voltage:
                voltage['model'].append([ stim, peak ])
            else:
                voltage['model'] = [ stim, peak ]
    except:
        pass
