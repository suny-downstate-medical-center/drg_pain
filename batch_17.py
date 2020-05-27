from netpyne import specs
from netpyne.batch import Batch

params = specs.ODict()

params['freq'] = range(5, 25)

b = Batch(params = params, cfgFile = 'cfg.py', netParamsFile = 'netParams.py')

b.batchLabel = 'freq'
b.saveFolder = 'freq_batch'
b.method = 'grid'
b.runCfg = {'type': 'mpi_bulletin', 'script': 'init.py', 'skip': True}

b.run()