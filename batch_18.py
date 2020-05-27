from netpyne import specs
from netpyne.batch import Batch
import numpy as np

params = specs.ODict()

params['mn1p8'] = np.linspace(0.5, 1, 6)

b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'freq'
b.saveFolder = 'freq_batch'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()