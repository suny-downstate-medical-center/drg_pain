from netpyne import specs
from netpyne.batch import Batch
import numpy as np

params = specs.ODict()

params['freq'] = 1
params['npulses'] = 1
params['duration'] = 50

params['mttxs'] = [x for x in np.linspace(0.5, 1.0, 6)]
#params['mn1p8'] = [x for x in np.linspace(0.5, 1.0, 6)]
b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'mttxs'
b.saveFolder = 'mttxs_batch'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()
