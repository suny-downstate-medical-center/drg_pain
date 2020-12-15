from neuron import h
from genrn import genrn

mandgeSomaRule = {
 'label': 'mandge',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.load_file("tautables.hoc")',
#     'cai0_ca_ion': 0.000136,
     'h.celsius = 22.0',
#     'cli0_cl_ion': 40.0,
#     'clo0_cl_ion': 145.0,
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
           'kaslow': {'gbar': 0.00136}, 'kdr': {'gbar': 0.002688},
           'kmtype': {'gbar': 0.0001}, 'knatype': {'gbar': 1e-05},
           'nakpump': {'gbar': 0.001, 'capm': 1.5481245576786977},
           'nav1p7': {'gbar': 0.018},
           'nav1p8': {'gbar': 0.026},
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

tigerholmCableRule = {
 'label': 'tigerholm',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.v_init = -60'],
 'secs': {'peri': { 'Ra': 35.5, 'cm': 1, 'nseg': 257, 'L': 5000, 'diam': 0.8  },
          'stem': { 'Ra': 35.5, 'cm': 1, 'nseg': 3  , 'L': 75  , 'diam': 1.4  },
          'soma': { 'Ra': 35.5, 'cm': 1, 'nseg': 1  , 'L': 24.0, 'diam': 24.0 },
          'cntr': { 'Ra': 35.5, 'cm': 1, 'nseg': 363, 'L': 5000, 'diam': 0.4  }},
 'ions': {'k': {'e': -83.7, 'i': 145.0, 'o': 5.4},
          'na':{'e': 72.5, 'i': 154.0, 'o': 8.9}},
 'mechs': {'ks': {'gbar': 0.0069733},
           'kf': {'gbar': 0.012756},
           'h' : {'gbar': 0.0025377},
           'nav1p7': {'gbar': 0.10664},
#           'nattxsT': {'gbar': 0.10664},
           'nav1p8T': {'gbar': 0.24271},
           'nav1p9T': {'gbar': 9.4779e-05},
           'nakpump': {'smalla': -0.0047891},
           'kdrT': {'gbar': 0.018002},
           'kna': {'gbar': 0.00042},
           'naoi': {'theta': 0.029},
           'koi': {'theta': 0.029},
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

# Mandge and Machanda 2019 model
mandgeSomaRule = {
 'label': 'mandge',
 'globals': [
     'h.load_file("stdrun.hoc")',
     'h.load_file("tautables.hoc")',
#     'cai0_ca_ion': 0.000136,
     'h.celsius = 22.0',
#     'cli0_cl_ion': 40.0,
#     'clo0_cl_ion': 145.0,
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
#        print('exec: %s' %(execstr))
        exec(execstr)

def createSoma( cellRule = somaRule):
    hInit(cellRule['globals'])
    cell = genrn( h = h, v_init = cellRule['v_init'],
                  secs = cellRule['secs'], mechs = cellRule['mechs'],
                  ions = cellRule['ions'], cons = ())
    cell('soma').sec.e_pas = -52.4
    return cell

def createCable( cellRule = tigerholmCableRule, v_init = -60):
    hInit(cellRule['globals'])
    cell = genrn( h = h, v_init = cellRule['v_init'],
                  secs = {'peri': cellRule['secs']['peri']}, mechs = cellRule['mechs'],
                  ions = cellRule['ions'], cons = ())
#     initialize voltages to v_init
    cell.h.finitialize(v_init)
    ina = cell('peri')(0.5).ina
    ena = cell('peri')(0.5).ena
    ik  = cell('peri')(0.5).ik
    ek  = cell('peri')(0.5).ek
    cell('peri').sec.gnaleak_leak = ina / (v_init - ena)
    cell('peri').sec.gkleak_leak  = ik  / (v_init - ek )
    return cell

if __name__=='__main__':
#    from pprint import pprint
    soma = {}
    soma[0] = createSoma(somaRule)
    soma[1] = createSoma(choiSomaRule)
    soma[2] = createSoma(mandgeSomaRule)

#    pprint(soma.get_dict())

"""

bladder_e_pas = {
    -80.0: -82.58602364872561,
    -79.5: -81.84335640030233,
    -79.0: -81.09958631509333,
    -78.5: -80.3554625915654,
    -78.0: -79.61054212701941,
    -77.5: -78.86475327198326,
    -77.0: -78.1185901413151,
    -76.5: -77.37095449636755,
    -76.0: -76.62349459036982,
    -75.5: -75.87387344502237,
    -75.0: -75.12511455625227,
    -74.5: -74.37342456827207,
    -74.0: -73.62342589675681,
    -73.5: -72.86964681577395,
    -73.0: -72.11853311788032,
    -72.5: -71.36270990866063,
    -72.0: -70.61066944826644,
    -71.5: -69.85290817816734,
    -71.0: -69.10018393296744,
    -70.5: -68.34064101113115,
    -70.0: -67.5875148229774,
    -69.5: -66.82637932447555,
    -69.0: -66.0731488279455,
    -68.5: -65.31061769034552,
    -68.0: -64.55756589610853,
    -67.5: -63.793811736997114,
    -67.0: -63.041169087318536,
    -66.5: -62.27630026321314,
    -66.0: -61.52419882326035,
    -65.5: -60.75821113971865,
    -65.0: -60.00663034953325,
    -64.5: -59.23934954795288,
    -64.0: -58.48805264712351,
    -63.5: -57.71906644675432,
    -63.0: -56.96752631001005,
    -62.5: -56.196104386448894,
    -62.0: -55.44341708768021,
    -61.5: -54.668416933537564,
    -61.0: -53.91320090135804,
    -60.5: -53.132957051361856,
    -60.0: -52.37323520244399,
    -59.5: -51.58542882588469,
    -59.0: -50.8184905752899,
    -58.5: -50.019995970089816,
    -58.0: -49.24223554880246,
    -57.5: -48.42893969198688,
    -57.0: -47.63566683507946,
    -56.5: -46.80225806854398,
    -56.0: -45.987477105010825,
    -55.5: -45.127199779850855,
    -55.0: -44.2833540171946,
    -54.5: -43.38772856713264,
    -54.0: -42.505409792747805,
    -53.5: -41.56392415436852,
    -53.0: -40.631554119618386,
    -52.5: -39.63134507941917,
    -52.0: -38.634849576726026,
    -51.5: -37.560412257396266,
    -51.0: -36.48292957476617,
    -50.5: -35.31591319101153,
    -50.0: -34.13759990671626,
    -49.5: -32.85674643965517,
    -49.0: -31.55474097865085,
    -48.5: -30.135968260666502,
    -48.0: -28.6845114348951,
    -47.5: -27.101029465282174,
    -47.0: -25.471618053695543,
    -46.5: -23.693878377027193,
    -46.0: -21.85523230129037,
    -45.5: -19.850578683062025,
    -45.0: -17.76828002718218,
    -44.5: -15.500403893386643,
    -44.0: -13.136324508045245,
    -43.5: -10.564827149983856,
    -43.0: -7.876676191409267,
    -42.5: -4.95701215249742,
    -42.0: -1.898300018337622,
    -41.5: 1.41781380967479,
    -41.0: 4.897309598462009,
    -40.5: 8.6610898868119,
    -40.0: 12.614441212321758}
def npSoma( mulnattxs = 1, mulnav1p8 = 1 , mulnav1p9 = 1, v_init = -53.5 ):
    hInit()
    cell = genrn(**bladderCellArgs)
    cell.soma.gbar_nattxs *= mulnattxs
    cell.soma.gbar_nav1p8 *= mulnav1p8
    cell.soma.gbar_nav1p9 *= mulnav1p9
    cell.soma.e_pas = bladder_e_pas[v_init]
    cell.h.finitialize(v_init)
    cell.h.fcurrent()
    print("initialize cell at %s mV" %(v_init))
    print("e_pas at %s mV" %(cell.soma.e_pas))
    # inflammatory changes
    # cell.soma.gbar_nav1p8 = 0.06   # 0.0087177 -> 0.06
    # cell.soma.gbar_kaslow = 0.0001 # 0.00136   -> 0.0001
    # cell.soma.gbar_kdr    = 0.001  # 0.002688  -> 0.001
    return cell

def npSomaMut( wtp = 1 ):
    hInit()
    cell = genrn(**bladderCellArgs)
    gbar_nattxs = 0.0001 * (wtp)
    gbar_navmut = 0.0001 * (1 - wtp)
    cell.edit_mechs('all', 'nattxs', 'gbar', gbar_nattxs)
    cell.insert_mech(sec='soma', mech='navmut', ions={'nak': {'e': -15.87}}, params={'gbar': gbar_navmut})
    return cell

def npTJ( mulnattxs = 1, mulnav1p8 = 1, mulnav1p9 = 1 ):
    hInit()
    cell = genrn(**tjCellArgs)
    gbar_nattxs = 0.0001 * mulnattxs
    gbar_nav1p8 = 0.0087177 * mulnav1p8
    gbar_nav1p9 = 1e-5 * mulnav1p9
    cell.edit_mechs('all', 'nattxs', 'gbar', gbar_nattxs)
    cell.edit_mechs('all', 'nav1p8', 'gbar', gbar_nav1p8)
    cell.edit_mechs('all', 'nav1p9', 'gbar', gbar_nav1p9)
    return cell
"""