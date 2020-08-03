from netpyne import sim
args = {'simConfigDefault': 'cfgIP.py',
        'netParamsDefault': 'npIP.py'}
cfg, netParams = sim.readCmdLineArgs(**args)
sim.create(simConfig = cfg, netParams = netParams)
sim.simulate()
sim.analyze()
