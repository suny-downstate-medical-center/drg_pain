from netpyne import sim

cfg, netParams = sim.readCmdLineArgs()
sim.create(simConfig = cfg, netParams = netParams)
sim.simulate()
sim.analyze()
