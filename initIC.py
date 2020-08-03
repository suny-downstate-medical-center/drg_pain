from netpyne import sim
args = {'simConfigDefault': 'cfgIC.py',
        'netParamsDefault': 'npIC.py'}
cfg, netParams = sim.readCmdLineArgs(**args)
sim.create(simConfig = cfg, netParams = netParams)
sim.simulate()
sim.analyze()
