UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX kdr
    USEION k READ ek WRITE ik
    RANGE gkbar, gk, ik
    RANGE ninf, ntau

:    RANGE q10
}

PARAMETER{ 
    gkbar  = 0.0035 (S/cm2)
:    q10    = 2.5 (1)
}

ASSIGNED {
	celsius (degC)
	v (mV)
    ik (mA/cm2)
    ek (mV)

    gk (S/cm2)

    nalpha (1/ms)
    nbeta (1/ms)

    ninf (1)
    ntau (ms)

:    tadj (1)

}

STATE{
    n
}

UNITSOFF

INITIAL{
    settables(v)
:    tadj = q10 ^ ((celsius - 22) / 10)
    n = ninf

}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gk = gkbar * n
    ik = gk * (v - ek)
}

DERIVATIVE states{
    settables(v)
    n' = (ninf - n) / ntau
}


PROCEDURE settables(v (mV)){
    TABLE ninf, ntau
:    DEPEND celsius
    FROM -100 TO 100 WITH 200

    nalpha = 0.001265 * (v + 14.273)/(1 - exp((v + 14.273) / -10))
    nbeta  = 0.125 * exp((v + 55) / -2.5)

    ninf   = 1 / (1 + exp((v + 14.62) / -18.38 ))
    ntau   = 1 / (nalpha + nbeta) + 1
:    ntau   = 1 / (nalpha + nbeta) / tadj
}

UNITSON

:The KDR current was defined as: IKDR = gKDR * n * (V - Ek), where gKDR is the delayed rectifier potassium conductance 
:and n is a dimensionless activation variable that varies between 0 and 1. The kinetic characterization of the channel
:described by Schild et al. (1994) has been used with alphan = 0.001265 * (V + 14.273)/{1 - exp[(V + 14.273)/-10]}; 
:betan = 0.125 * exp(V + 55/-2.5); and ninf = 1/{1 + exp[(V + 14.62)/-18.38]}. The peak conductance for KDR (gKDR) was 
:set to 0.0035 S/cm2, which corresponds to 6 nA potassium current at 0 mV.

:from MATLAB port, where does this +1 at the end come from for ntau?
:it actually comes from the original paper -- this should be mentioned but is not
:1.0/ (0.001265*(v+14.3)/(1.0-exp((v+14.3)/-10.0))+0.125*exp((v+55.0)/-2.5)) +1.0