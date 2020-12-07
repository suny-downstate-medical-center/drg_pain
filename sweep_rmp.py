import cells
import matplotlib.pyplot as plt
import numpy as np
soma = cells.npSoma()
ions = ['ca', 'cl', 'h', 'k', 'na']
rmps = np.linspace(-80,-40, 81)
data = {}
data_pas = {}
# note that
# ca: bkca, cadyn, skca3, trpm8
# na: cadyn, knatype
# are empty
for ion in ions:
    data[ion] = {}
    for mech in soma('soma').ions[ion]['mechs']:
        data[ion][mech] = []
    data['i_net'] = []
    data['e_pas'] = []
    data['rmp'] = rmps

for rmp in rmps:
    rmpdata = soma.init_v(rmp, ions)['soma']
    for mech in rmpdata:
        try:
            for ion in rmpdata[mech]:
                if rmpdata[mech][ion]:
                    data[ion][mech].append(rmpdata[mech][ion])
        except:
            data[mech].append(rmpdata[mech])
    data_pas[rmp] = rmpdata['e_pas']

for ion in ions:
    plt.title(ion)
    for mech in data[ion]:
        if data[ion][mech]:
            plt.plot(rmps, data[ion][mech], label=mech)
    plt.legend()
    plt.xlabel("membrane potential (mV)")
    plt.ylabel("steady state current (mA/cm2)")
    plt.show()

plt.title('e_pas')
plt.plot(rmps, data['e_pas'])
plt.xlabel("membrane potential (mV)")
plt.ylabel("e_pas (mV)")
plt.show()