UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX ka
    USEION k READ ek WRITE ik
    RANGE gkbar, gk, ik
    RANGE ninf, ntau, hinf, htau

:    RANGE q10
}

PARAMETER{ 
    gkbar  = 0.0055 (S/cm2)
:    q10    = 2.5
}

ASSIGNED {
	celsius (degC)
	v (mV)
    ik (mA/cm2)
    ek (mV)

    gk (S/cm2)

    ninf (1)
    ntau (1/ms)

    hinf (1)
    htau (1/ms)

:    tadj (1)

}

STATE{
    n h
}


UNITSOFF

INITIAL{
    settables(v)
:    tadj = q10^((celsius - 22) / 10)
    n = ninf
    h = hinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gk = gkbar * n * h 
    ik = gk * (v - ek)
}

DERIVATIVE states{
    settables(v)
    n' = (ninf - n) / ntau
    h' = (hinf - h) / htau
}


PROCEDURE settables(v (mV)){
    TABLE ninf, ntau, hinf, htau
:    DEPEND celsius
    FROM -100 TO 100 WITH 200

    ninf   = 1 / (1 + exp(-(v + 5.4) / 16.4))^4
    ntau   = 0.25 + 10.04 * exp(-(v + 24.67)^2 / 2422.08)
:    ntau   = (0.25 + 10.04 * exp(-(v + 24.67)^2 / 2422.08)) / tadj

    hinf   = 1 / (1 + exp((v + 49.9) / 4.6 ))
    htau   = 20 + 50 * exp(-(v + 40)^2 / 3200)

    if (htau < 5) {
        htau = 5
    }
:    htau   = (20 + 50 * exp(-((v + 40)^2)/(2 * 40^2))) / tadj

:    ntau   = 1 / (nalpha + nbeta) / tadj

}

UNITSON

:The KA current was defined as: IKA = gKA * n * h * (V - Ek), where gKA is the A-type potassium conductance and n and h
:are dimensionless activation and inactivation variables, respectively, that vary between 0 and 1. The kinetic 
:characterization of the channel described by Gold et al. (1996b) has been used with dn/dt = (ninf - n)/ntau;
:dh/dt = (hinf - h)/htau; ninf = (1/(1 + exp(-(v + 5.4)/16.4)))^4;
:ntau= (0.25 + 10.04 * exp(-(((v + 24.67)^2]/(2 * 34.8^2))); hinf = 1/(1 + exp((v + 49.9)/4.6)); 
:htau = (20 + 50 * exp(- ((v + 40)^2]/(2 * 40^2))); if htau < 5 then htau = 5. The peak conductance for KA (gKA) 
:was set to 0.0055 S/cm2, which corresponds to 1 nA potassium current at 0 mV.