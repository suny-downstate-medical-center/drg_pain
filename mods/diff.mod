COMMENT
Longitudinal diffusion and integration of sodium (no buffering)
make sure to use sufficiently high nseg
(equivalent modified euler with standard method and
equivalent to diagonalized linear solver with CVODE )
From Canavier et al. 1999
ENDCOMMENT

NEURON {
   SUFFIX diff
   USEION na READ ina WRITE nai
   USEION k READ ik WRITE ki
   USEION ca READ ica WRITE cai
   RANGE D
}

UNITS {
   (molar) = (1/liter)
   (mM) = (millimolar)
   (um) = (micron)
   FARADAY = (faraday) (coulomb)
   PI = (pi) (1)
}

PARAMETER {
   D = .6 (um2/ms)
}

ASSIGNED {
   ina (mA/cm2)
   ik (mA/cm2)
   ica (mA/cm2)
   diam (um)
}


INITIAL {
     nai = 15
     ki = 150
     cai = 0.000136
}

STATE {
   nai (mM)
   ki (mM)
   cai (mM)
}

BREAKPOINT {
   SOLVE conc METHOD sparse
}

KINETIC conc {
   COMPARTMENT PI*diam*diam/4 {nai}
   LONGITUDINAL_DIFFUSION D {nai}
   ~ nai << (-ina/(FARADAY)*PI*diam*(1e4))
   ~ ki << (-ik/(FARADAY)*PI*diam*(1e4))
   ~ cai << (-ica/(FARADAY)*PI*diam*(1e4))
}