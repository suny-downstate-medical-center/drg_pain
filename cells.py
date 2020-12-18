from neuron import h
from genrn import genrn

# custom model
somaRule = {
 'label': 'custom',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.load_file("tautables.hoc")',
     'h.celsius = 22.0',
     'h.ki0_k_ion = 140.0',
     'h.ko0_k_ion = 5.0',
     'h.nao0_na_ion = 150.0',
#     'h.v_init = -53.5'],
     'h.v_init = -60'],
 'secs': {'soma': {'L': 24.0, 'Ra': 100.0, 'cm': 1.5481245576786977, 'diam': 24.0, 'nseg': 1}},
 'ions': {'ca': {'e': 132.4579341637009, 'i': 0.000136, 'o': 2.0},
          'caer': {'e': 0.0, 'i': 0.4, 'o': 1.0},
          'caip3r': {'e': 0.0, 'i': 0.000136, 'o': 1.0},
          'camt': {'e': 0.0, 'i': 0.0002, 'o': 1.0},
          'cl': {'e': -32.7, 'i': 40.0, 'o': 145.0},
          'h': {'e': -30.0, 'i': 1.0, 'o': 1.0},
          'ip3': {'e': 0.0, 'i': 1.0, 'o': 1.0},
          'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
          'na': {'e': 68.83, 'i': 10.0, 'o': 150.0}},
 'mechs': {'CaL': {'pmax': 2.75e-05, 'hca': 0.0},
           'CaN': {'pmax': 2.8e-05, 'a': 0.7326, 'hca': 0.0},
           'CaPQ': {'pmax': 8e-06}, 'CaR': {'pmax': 1e-08}, 'CaT': {'pmax': 1e-08},
           'bkca': {'gbar': 0.0009},
           'cacc': {'gbar': 1e-06},
           'cadyn': {'Bmer': 10.0, 'Bmmt': 0.065,
                     'Kmer': 0.5, 'Kmmt': 1e-05,
                     'jmaxsr': 3.5e-06,
                     'k1': 37400000.0, 'k2': 250000.0, 'k3': 500.0, 'k4': 5.0,
                     'kactip3': 0.0003, 'kcicr': 0.00198, 'kinhip3': 0.0002,
                     'kip3': 0.0008, 'kmcu': 0.000606, 'kna': 8.0,
                     'kncx': 0.035, 'konip3': 2.7, 'kpsr': 0.00027,
                     'ktcicr': 0.0006, 'nmcu': 2.3, 'pump0': 4.232e-13,
                     'vcicr': 5e-07, 'vmaxsr': 3.75e-06, 'vmcu': 1.4468e-06,
                     'vncx': 6e-05},
           'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
           'ip3dif': {},
           'kaslow': {'gbar': 0.0055}, 'kdr': {'gbar': 0.002688},
           'kmtype': {'gbar': 0.0001}, 'knatype': {'gbar': 1e-05},
           'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
           'nav1p7': {'gbar': 0.018},
           'nav1p8': {'gbar': 0.026},
           'nav1p9': {'gbar': 1e-05},
           'ncxsoma': {'ImaxNax': 1.1e-05, 'KcNacx': 1.38, 'KnNacx': 87.5},
           'pas': {'g': 0.0001, 'e': -52.37},
           'skca3': {'E50hsk3': 0.00042, 'gbar': 0.0009, 'hcsk3': 5.6,
                     'm': 0.0, 'm_sf': 128.0, 'm_vh': 24.0},
           'soce': {'pmax': 1e-09},
           'trpm8': {'C': 67.0, 'em8': 0.0, 'gbar': 1e-07,
                     'p_ca': 0.01, 'z': 0.65}},
 'v_init': -60.0}

# Tigerholm
tigerholmCableRule = {
 'label': 'tigerholm',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.v_init = -60'],
 'secs': {'peri' : { 'Ra': 35.5, 'cm': 1, 'nseg':  19, 'L':  500, 'diam': 0.8  },#
          'stem' : { 'Ra': 35.5, 'cm': 1, 'nseg': 3  , 'L':   75, 'diam': 1.4  },# nseg calculated with:
          'soma' : { 'Ra': 35.5, 'cm': 1, 'nseg': 1  , 'L':   24, 'diam': 24.0 },# frequency: 100
          'cntr' : { 'Ra': 35.5, 'cm': 1, 'nseg':  25, 'L':  500, 'diam': 0.4  },# d_lambda : 0.1
          'lperi': { 'Ra': 35.5, 'cm': 1, 'nseg': 179, 'L': 5000, 'diam': 0.8  },#
          'lcntr': { 'Ra': 35.5, 'cm': 1, 'nseg': 251, 'L': 5000, 'diam': 0.4  },
          'cable': { 'Ra': 35.5, 'cm': 1, 'nseg':  37, 'L': 1000, 'diam': 0.8  }},
 'ions': {'k': {'e': -83.7, 'i': 145.0, 'o': 5.4},
          'na':{'e': 72.5, 'i': 154.0, 'o': 8.9}},
 'mechs': {'ks': {'gbar': 0.0069733},
           'kf': {'gbar': 0.012756},
           'h' : {'gbar': 0.0025377},
           'nav1p7': {'gbar': 0.10664},
#           'nattxsT': {'gbar': 0.10664},
           'nav1p8T': {'gbar': 0.24271},
           'nav1p9T': {'gbar': 9.4779e-05},
           'nakpumpT': {'smalla': -0.0047891},
           'kdrT': {'gbar': 0.018002},
           'kna': {'gbar': 0.00042},
           'naoi': {'theta': 0.029}, # doesn't work as is, theta is not a RANGE
           'koi': {'theta': 0.029},  # doesn't work as is, theta is not a RANGE
           'leak': {},
           'extrapump': {}},
 'v_init': -60.0,
 'cons': (('stem', 'peri'),
          ('soma', 'stem'),
          ('cntr', 'peri'))
}

# Choi
choiSomaRule = {
 'label': 'choi',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.celsius = 22.0',
     'h.v_init = -60.0'],
 'secs': {'soma': {'L': 30.0, 'Ra': 123.0, 'cm': 1.5481245576786977, 'diam': 23.0, 'nseg': 1}},
 'ions': {'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
          'na': {'e': 67.12, 'i': 10.0, 'o': 140.0}},
 'mechs': {'kaslow': {'gbar': 0.0055}, 'kdr': {'gbar': 0.0035},
           'nav1p7': {'gbar': 0.018},
           'nav1p8': {'gbar': 0.026},
           'nav1p9': {'gbar': 1e-05},
           'pas': {'g': 0.0000575, 'e': -58.91}},
 'v_init': -60}

# Mandge
mandgeSomaRule = {
 'label': 'mandge',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.load_file("tautables.hoc")',
     'h.celsius = 22.0',
     'h.ki0_k_ion = 140.0',
     'h.ko0_k_ion = 5.0',
     'h.nao0_na_ion = 150.0',
     'h.v_init = -60'],
 'secs': {'soma': {'L': 24.0, 'Ra': 100.0, 'cm': 1.5481245576786977, 'diam': 24.0, 'nseg': 1}},
 'ions': {'ca': {'e': 132.4579341637009, 'i': 0.000136, 'o': 2.0},
          'caer': {'e': 0.0, 'i': 0.4, 'o': 1.0},
          'caip3r': {'e': 0.0, 'i': 0.000136, 'o': 1.0},
          'camt': {'e': 0.0, 'i': 0.0002, 'o': 1.0},
          'cl': {'e': -32.7, 'i': 40.0, 'o': 145.0},
          'h': {'e': -30.0, 'i': 1.0, 'o': 1.0},
          'ip3': {'e': 0.0, 'i': 1.0, 'o': 1.0},
          'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
          'na': {'e': 68.83, 'i': 10.0, 'o': 150.0}},
 'mechs': {'CaL': {'pmax': 2.75e-05, 'hca': 0.0},
           'CaN': {'pmax': 2.8e-05, 'a': 0.7326, 'hca': 0.0},
           'CaPQ': {'pmax': 8e-06}, 'CaR': {'pmax': 1e-08}, 'CaT': {'pmax': 1e-08},
           'bkca': {'gbar': 0.0009},
           'cacc': {'gbar': 1e-06},
           'cadyn': {'Bmer': 10.0, 'Bmmt': 0.065,
                     'Kmer': 0.5, 'Kmmt': 1e-05,
                     'jmaxsr': 3.5e-06,
                     'k1': 37400000.0, 'k2': 250000.0, 'k3': 500.0, 'k4': 5.0,
                     'kactip3': 0.0003, 'kcicr': 0.00198, 'kinhip3': 0.0002,
                     'kip3': 0.0008, 'kmcu': 0.000606, 'kna': 8.0,
                     'kncx': 0.035, 'konip3': 2.7, 'kpsr': 0.00027,
                     'ktcicr': 0.0006, 'nmcu': 2.3, 'pump0': 4.232e-13,
                     'vcicr': 5e-07, 'vmaxsr': 3.75e-06, 'vmcu': 1.4468e-06,
                     'vncx': 6e-05},
           'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
           'ip3dif': {},
           'kaslow': {'gbar': 0.00136}, 'kdr': {'gbar': 0.002688},
           'kmtype': {'gbar': 0.0001}, 'knatype': {'gbar': 1e-05},
           'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
           'nav1p7': {'gbar': 0.0001},
#           'nattxs': {'gbar': 0.0001},
           'nav1p8': {'gbar': 0.0087177},
           'nav1p9': {'gbar': 1e-05},
           'ncxsoma': {'ImaxNax': 1.1e-05, 'KcNacx': 1.38, 'KnNacx': 87.5},
#           'pas': {'g': 0.0001, 'e': -41.583},
           'pas': {'g': 0.0001, 'e': -52.37},
           'skca3': {'E50hsk3': 0.00042, 'gbar': 0.0009, 'hcsk3': 5.6,
                     'm': 0.0, 'm_sf': 128.0, 'm_vh': 24.0},
           'soce': {'pmax': 1e-09},
           'trpm8': {'C': 67.0, 'em8': 0.0, 'gbar': 1e-07,
                     'p_ca': 0.01, 'z': 0.65}},
 'v_init': -60.0}
# 'v_init': -53.5}

def hInit( execstrs ):
    for execstr in execstrs:
        exec(execstr)

def createSoma( cellRule = somaRule):
    hInit(cellRule['globals'])
    cell = genrn( h = h, v_init = cellRule['v_init'],
                  secs = cellRule['secs'], mechs = cellRule['mechs'],
                  ions = cellRule['ions'], cons = ())
    cell('soma').sec.e_pas = -52.4
    return cell

def createCable( cableRule = tigerholmCableRule, v_init = -60):
    hInit(cableRule['globals'])
    cable = genrn( h = h, v_init = cableRule['v_init'],
                  secs = {'cable': cableRule['secs']['cable']}, mechs = cableRule['mechs'],
                  ions = cableRule['ions'], cons = ())
#     initialize voltages to v_init
    cable.h.finitialize(v_init)
    ina = cable('cable')(0.5).ina
    ena = cable('cable')(0.5).ena
    ik  = cable('cable')(0.5).ik
    ek  = cable('cable')(0.5).ek
    cable('cable').sec.gnaleak_leak = ina / (v_init - ena)
    cable('cable').sec.gkleak_leak  = -ik / (v_init - ek )
    return cable

def createTJ( cableRule = tigerholmCableRule, somaRule = somaRule, v_init = -60 ):
    hInit(somaRule['globals'])
    cell = genrn( h = h, v_init = -60,
                  secs = {'cblperi': cableRule['secs']['peri'],
                          'cblstem': cableRule['secs']['stem'],
                          'drgsoma':  somaRule['secs']['soma'],
                          'cblcntr': cableRule['secs']['cntr']},
                  cons = (('cblstem', 'cblperi'),
                          ('drgsoma', 'cblstem'),
                          ('cblcntr', 'cblperi')),
                  ions = somaRule['ions'],
                  mechs = {} )
    cell.initialize_mechs('cbl', cableRule['mechs'])
    cell.initialize_mechs('drg', somaRule['mechs'])
    cell.initialize_ionprops()

    cell.h.finitialize(v_init)
    for sec in ['cblperi', 'cblstem', 'cblcntr']:
        cell(sec)(0.5).ena = 50
        ina = cell(sec)(0.5).ina
        ena = cell(sec)(0.5).ena
        ik  = cell(sec)(0.5).ik
        ek  = cell(sec)(0.5).ek
        cell(sec).sec.gnaleak_leak = ina / (v_init - ena)
        cell(sec).sec.gkleak_leak  = -ik / (v_init - ek )
    return cell

if __name__=='__main__':
    soma = {}
    soma[0] = createSoma(somaRule)
    soma[1] = createSoma(choiSomaRule)
    soma[2] = createSoma(mandgeSomaRule)
    cable = {}
    cable[0] = createCable(tigerholmCableRule)
    tj = {}
    tj[0] = createTJ(tigerholmCableRule, somaRule)