from neuron import h
import numpy as np
import matplotlib.pyplot as plt

h.load_file("stdrun.hoc")
h.load_file("tautables.hoc")
h.celsius = 22

vs = []
test = h.Section(name='test')
test.insert('nav1p7')
test.ashft_nav1p7 = 40
test_minfs = []

ctrl = h.Section(name='ctrl')
ctrl.insert('nav1p7')
ctrl.ashft_nav1p7 = 0
ctrl_minfs = []


for v in np.linspace(-50, 50, 100):
    vs.append(v)
    h.finitialize(v)
    test_minfs.append(test.minf_nav1p7)
    ctrl_minfs.append(-ctrl.minf_nav1p7)

plt.plot(vs , test_minfs)
plt.plot(vs , ctrl_minfs)
plt.show()