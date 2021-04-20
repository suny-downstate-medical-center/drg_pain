from neuron import h

from netpyne.specs import NetParams

netParams = NetParams()

cell = netParams.importCellParams(label= 'cable', conds={'cellType': 'cable'},
                                  fileName= 'CV.hoc', cellName= 'run_nrn_script',
                                  cellArgs= {'type': 2})
h.load_file('CV.hoc')