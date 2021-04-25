from neuron import h
from genrn import genrn

# test nav rule
navRule = {
 'label': 'nav',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.celsius = 22.0'
 ]
}

# custom model
somaRule = {
 'label': 'customSoma',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.load_file("tautables.hoc")',
     'h.celsius = 22.0',
     'h.ki0_k_ion = 140.0',
     'h.ko0_k_ion = 5.0',
     'h.nao0_na_ion = 150.0',
#     'h.v_init = -53.5'],
     'h.v_init = -60'],
 # 'secs': {'soma': {'L': 30.0, 'Ra': 123.0, 'cm': 1.5, 'diam': 23.0, 'nseg': 1}},
 'secs': {'soma': {'L': 24.0, 'Ra': 123.0, 'cm': 1.5, 'diam': 24.0, 'nseg': 1}},
 'ions': {'ca': {'e': 132.4579341637009, 'i': 0.000136, 'o': 2.0},
          'caer': {'e': 0.0, 'i': 0.4, 'o': 1.0},
          'caip3r': {'e': 0.0, 'i': 0.000136, 'o': 1.0},
          'camt': {'e': 0.0, 'i': 0.0002, 'o': 1.0},
          'cl': {'e': -32.7, 'i': 40.0, 'o': 145.0},
          'h': {'e': -30.0, 'i': 1.0, 'o': 1.0},
          'ip3': {'e': 0.0, 'i': 1.0, 'o': 1.0},
          'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
          'na': {'e': 67.1, 'i': 10.0, 'o': 150.0}},
 'mechs': {'CaL': {'pmax': 2.75e-05, 'hca': 0.0},
           'CaN': {'pmax': 2.8e-05, 'a': 0.7326, 'hca': 0.0},
           'CaPQ': {'pmax': 8e-06}, 'CaR': {'pmax': 1e-08}, 'CaT': {'pmax': 1e-08},
           'bkca': {'gbar': 0.0009},
           'cacc': {'gbar': 1e-06},
           'cadyn': {'Bmer': 10.0, 'Bmmt': 0.065, 'Kmer': 0.5, 'Kmmt': 1e-05, 'jmaxsr': 3.5e-06, 'k1': 37400000.0, 'k2': 250000.0, 'k3': 500.0, 'k4': 5.0,
                     'kactip3': 0.0003, 'kcicr': 0.00198, 'kinhip3': 0.0002, 'kip3': 0.0008, 'kmcu': 0.000606, 'kna': 8.0, 'kncx': 0.035, 'konip3': 2.7,
                     'kpsr': 0.00027, 'ktcicr': 0.0006, 'nmcu': 2.3, 'pump0': 4.232e-13, 'vcicr': 5e-07, 'vmaxsr': 3.75e-06, 'vmcu': 1.4468e-06, 'vncx': 6e-05},
           'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
           'ip3dif': {},
           'kas': {'gbar': 0.009},
           # 'kaslow': {'gbar': 0.00136},
           'kdr': {'gbar': 0.00576},
           'kmtype': {'gbar': 0.0001}, 'knatype': {'gbar': 1e-05},
           'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
           'nav1p7': {'gbar': 0.018 * 1.2},
           'nav1p8': {'gbar': 0.026 * 1.2},
           # 'nav1p7c':{'gbar': 0.018, 'ashft': 0, 'ishft': 0}, # ashft, ishft -> activation shift, inactivation shift
           'nav1p9': {'gbar': 1e-05},
           'ncxsoma': {'ImaxNax': 1.1e-05, 'KcNacx': 1.38, 'KnNacx': 87.5},
           # 'pas': {'g': 0.0000575, 'e': -52.37},
           'pas': {'g': 0.0001, 'e': -52.37},
           'skca3': {'E50hsk3': 0.00042, 'gbar': 0.0009, 'hcsk3': 5.6,
                     'm': 0.0, 'm_sf': 128.0, 'm_vh': 24.0},
           'soce': {'pmax': 1e-09},
           'trpm8': {'C': 67.0, 'em8': 0.0, 'gbar': 1e-07,
                     'p_ca': 0.01, 'z': 0.65}},
 'v_init': -60.0}

# custom model with temperature dependancy
somaRuleTD = {
 'label': 'customSoma(tadj)',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.load_file("tautables.hoc")',
     'h.celsius = 37.0',
     'h.ki0_k_ion = 140.0',
     'h.ko0_k_ion = 5.0',
     'h.nao0_na_ion = 150.0',
     'h.v_init = -60'],
 # 'secs': {'soma': {'L': 30.0, 'Ra': 123.0, 'cm': 1.5, 'diam': 23.0, 'nseg': 1}},
 'secs': {'soma': {'L': 24.0, 'Ra': 123.0, 'cm': 1.5, 'diam': 24.0, 'nseg': 1}},
 'ions': {'ca': {'e': 132.4579341637009, 'i': 0.000136, 'o': 2.0},
          'caer': {'e': 0.0, 'i': 0.4, 'o': 1.0},
          'caip3r': {'e': 0.0, 'i': 0.000136, 'o': 1.0},
          'camt': {'e': 0.0, 'i': 0.0002, 'o': 1.0},
          'cl': {'e': -32.7, 'i': 40.0, 'o': 145.0},
          'h': {'e': -30.0, 'i': 1.0, 'o': 1.0},
          'ip3': {'e': 0.0, 'i': 1.0, 'o': 1.0},
          'k': {'e': -84.7, 'i': 140.0, 'o': 5.0},
          'na': {'e': 67.1, 'i': 10.0, 'o': 150.0}},
 'mechs': {'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
           'nav1p7mut': {'gbar': 0.018 * 1.2 }, # mutant NaV 1.7
           'nav1p7': {'gbar': 0.018 * 1.2 },  # NaV 1.7
           'nav1p8': {'gbar': 0.026 * 1.2 },  # NaV 1.8
           'nav1p9': {'gbar': 1e-05},  # NaV 1.9
           'kdr': {'gbar': 0.00576},  # KDR (delayed rectifier calcium channel - "KCNJ"?)
           'kas': {'gbar': 0.009},    # KA
           'kmtype': {'gbar': 0.0001}, # KM (M type calcium channel - "KM/KCNQ")
           'knatype': {'gbar': 1e-05}, # KNA
           'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
           'CaL': {'pmax': 2.75e-05, 'hca': 0.0},
           'CaN': {'pmax': 2.8e-05, 'a': 0.7326, 'hca': 0.0},
           'bkca': {'gbar': 0.0009},
           'skca3': {'E50hsk3': 0.00042, 'gbar': 0.0009, 'hcsk3': 5.6,
                     'm': 0.0, 'm_sf': 128.0, 'm_vh': 24.0},
           'pas': {'g': 0.0001}},  # celsiusT
 'v_init': -60.0}

# custom cable rule
# channels for custom cable, NaV 1.7, 1.8, 1.9, KDR, KA, KM, KNa
cableRule = {
    'label': 'customCable',
    'globals': [
        'h.load_file("stdrun.hoc")',
        'h.v_init = -60'],
    'secs': {'peri' : {'Ra': 100, 'cm': 1.55, 'nseg': 37 , 'L': 500 , 'diam': 0.8},  #
             'stem' : {'Ra': 100, 'cm': 1.55, 'nseg': 5  , 'L': 75  , 'diam': 1.4},  # nseg calculated with:
             'soma' : {'Ra': 100, 'cm': 1.55, 'nseg': 1  , 'L': 24  , 'diam': 24.0}, # frequency: 100
             'cntr' : {'Ra': 100, 'cm': 1.55, 'nseg': 53 , 'L': 500 , 'diam': 0.4},  # d_lambda : 0.1
             'lperi': {'Ra': 100, 'cm': 1.55, 'nseg': 371, 'L': 5000, 'diam': 0.8},  #
             'lcntr': {'Ra': 100, 'cm': 1.55, 'nseg': 525, 'L': 5000, 'diam': 0.4},
             'cable': {'Ra': 100, 'cm': 1.55, 'nseg': 371 , 'L': 5000, 'diam': 0.8}},
    'ions': {'k': {'e': -83.7, 'i': 145.0, 'o': 5.4},
             'na': {'e': 72.5, 'i': 154.0, 'o': 8.9},
             'ca': {'e': 132.4579341637009, 'i': 0.000136, 'o': 2.0},
             'h': {'e': -30.0, 'i': 1.0, 'o': 1.0} },
    'mechs': {'hcn': {'gbarfast': 1.352e-05, 'gbarslow': 6.7615e-06},
              'nav1p7mut': {'gbar': 0.018 * 1.2 }, # mutant NaV 1.7
              'nav1p7': {'gbar': 0.018 * 1.2 * 2.0},  # NaV 1.7
              'nav1p8': {'gbar': 0.026 * 1.2 * 2.0},  # NaV 1.8
              'nav1p9': {'gbar': 1e-05},  # NaV 1.9
              'kdr': {'gbar': 0.00576},  # KDR
              'kas': {'gbar': 0.009},    # KA
              'kmtype': {'gbar': 0.0001}, # KM
              'knatype': {'gbar': 1e-05}, # KNA
              'CaL': {'pmax': 2.75e-05, 'hca': 0.0},
              'CaN': {'pmax': 2.8e-05, 'a': 0.7326, 'hca': 0.0},
              'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
              'pas': {'g': 0.0001},
              'bkca': {'gbar': 0.0009},
              'skca3': {'E50hsk3': 0.00042, 'gbar': 0.0009, 'hcsk3': 5.6,
                        'm': 0.0, 'm_sf': 128.0, 'm_vh': 24.0}},
    'v_init': -60.0,
    'cons': (('stem', 'peri'),
             ('soma', 'stem'),
             ('cntr', 'peri'))
}

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
          'lperi': { 'Ra': 35.5, 'cm': 1, 'nseg': 179, 'L': 5000, 'diam': 0.8  },
          'lcntr': { 'Ra': 35.5, 'cm': 1, 'nseg': 251, 'L': 5000, 'diam': 0.4  },
          'cable': { 'Ra': 35.5, 'cm': 1, 'nseg':  37, 'L': 1000, 'diam': 0.8  }},
 'ions': {'k': {'e': -83.7, 'i': 145.0, 'o': 5.4},
          'na':{'e': 72.5, 'i': 154.0, 'o': 8.9}},
 'mechs': {'ks': {'gbar': 0.0069733, 'celsiusT': 22},           # celsiusT
           'kf': {'gbar': 0.012756, 'celsiusT': 22},            # celsiusT
           'h' : {'gbar': 0.0025377, 'celsiusT': 22},           # celsiusT
           'nav1p7': {'gbar': 0.10664},
           'nattxsT': {'gbar': 0.00, 'celsiusT': 22},           # same as nav1p7, set gbar to 0
           'nav1p8T': {'gbar': 0.24271, 'celsiusT': 22},        # celsiusT
           'nav1p9T': {'gbar': 9.4779e-05, 'celsiusT': 22},     # celsiusT
           'nakpumpT': {'smalla': -0.0047891, 'celsiusT': 22},  # celsiusT
           'kdrT': {'gbar': 0.018002, 'celsiusT': 22},          # celsiusT
           'kna': {'gbar': 0.00042},            # no celsiusT
           'leak': {},
           'extrapump': {}},
           # 'naoi': {'theta': 0.029}, # doesn't work in original repo where theta is not a RANGE
           # 'koi': {'theta': 0.029}}, # doesn't work in original repo where theta is not a RANGE
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

def mInit( sec , v_init ):
    if hasattr(sec, 'e_pas'):
        i_net = sec.ik + sec.ina
        sec.e_pas = v_init + i_net / sec.g_pas
        print("SET: %s e_pas = %s" % (sec, sec.e_pas))
    elif hasattr( sec , 'pumpina_extrapump'):
        ina, ena = sec.ina, sec.ena
        ik, ek = sec.ik, sec.ek
        if - ina / (v_init - ena) < 0:
            sec.pumpina_extrapump = -ina
        else:
            sec.gnaleak_leak = -ina / (v_init - ena)
        if - ik / (v_init - ek) < 0:
            sec.pumpik_extrapump = -ik
        else:
            sec.gkleak_leak = -ik / (v_init - ek)
        print("SET: %s pump/leak" % (sec))

def createSoma( somaRule = somaRule, v_init = -60):
    print("creating soma model: %s" %(somaRule['label']))
    hInit(somaRule['globals'])
    cell = genrn( h = h, v_init = somaRule['v_init'],
                  secs = somaRule['secs'], mechs = somaRule['mechs'],
                  ions = somaRule['ions'], cons = ())
    h.finitialize(v_init)
    for sec_ in cell.secs:
        sec = cell(sec_).sec
        mInit(sec, v_init)
    return cell

def createCable( cableRule = cableRule, v_init = -60):
    print("creating cable model: %s" %(cableRule['label']))
    hInit(cableRule['globals'])
    cable = genrn( h = h, v_init = cableRule['v_init'],
                   secs = {'cable': cableRule['secs']['cable']}, mechs = cableRule['mechs'],
                   ions = cableRule['ions'], cons = ())
#     initialize voltages to v_init
    h.finitialize(v_init)
    for sec_ in cable.secs:
        sec = cable(sec_).sec
        mInit(sec, v_init)
    return cable

def createTJ( cableRule = cableRule, somaRule = somaRule, v_init = -60,
              mnav = 1.0, m1p7 = 1.0, m1p8 = 1.0, m1p9 = 1.0, mut = 0.0, ashft = 0.0, ishft = 0.0,
              mk = 1.0, mkca = 1.0, mkm = 1.0):
    print("creating TJ model: %s-%s" %(cableRule['label'], somaRule['label']))
    hInit(somaRule['globals'])
    cell = genrn( h = h, v_init = -60,
                  secs = {'cblperi': cableRule['secs']['peri'],
                          'drgstem': cableRule['secs']['stem'],
                          'drgsoma':  somaRule['secs']['soma'],
                          'cblcntr': cableRule['secs']['cntr']},
                  cons = (('drgstem', 'cblperi'),
                          ('drgsoma', 'drgstem'),
                          ('cblcntr', 'cblperi')),
                  ions = somaRule['ions'],
                  mechs = {} )
    cell.initialize_mechs('cbl', cableRule['mechs'])
    cell.initialize_mechs('drg', somaRule['mechs'])
    cell.initialize_ionprops()
    h.finitialize(v_init)
    print(cell)
    for sec_ in cell.secs:
        sec = cell(sec_).sec
        mInit(sec, v_init)
        sec.gbar_nav1p7     = sec.gbar_nav1p7    * mnav * m1p7 * (1-mut)
        sec.ashft_nav1p7    = ashft
        sec.ishft_nav1p7    = ishft
        sec.gbar_nav1p7mut  = sec.gbar_nav1p7mut * mnav * m1p7 * mut
        sec.ashft_nav1p7mut = ashft
        sec.ishft_nav1p7mut = ishft
        sec.gbar_nav1p8     = sec.gbar_nav1p8    * mnav * m1p8
        sec.gbar_nav1p9     = sec.gbar_nav1p9    * mnav * m1p9
    for sec_ in cell.tags['cbl']:
        sec = sec_.sec
        sec.gbar_bkca       = sec.gbar_bkca      * mk * mkca
        sec.gbar_kmtype     = sec.gbar_kmtype    * mk * mkm
    for sec_ in cell.tags['drg']:
        sec = sec_.sec
        sec.gbar_bkca       = sec.gbar_bkca      * mk * mkca
        sec.gbar_kmtype     = sec.gbar_kmtype    * mk * mkm

    return cell

if __name__=='__main__':
    from netpyne import specs
    from pprint import pprint
    netParams = specs.NetParams()
    tj = {}
    tj[0] = createTJ(cableRule, somaRuleTD)
