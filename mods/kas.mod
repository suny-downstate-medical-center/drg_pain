TITLE fast K current adopted from Sheets et al., 2007
COMMENT
KA taken from Sheets et al., 2007.

The KA current was defined as: IKA = gKA * n * h * (V - Ek), where gKA is the A-type potassium conductance and n and h
are dimensionless activation and inactivation variables, respectively, that vary between 0 and 1. The kinetic 
characterization of the channel described by Gold et al. (1996b) has been used with dn/dt = (ninf - n)/ntau;
dh/dt = (hinf - h)/htau; ninf = (1/(1 + exp(-(v + 5.4)/16.4)))^4;
ntau= (0.25 + 10.04 * exp(-(((v + 24.67)^2]/(2 * 34.8^2))); hinf = 1/(1 + exp((v + 49.9)/4.6)); 
htau = (20 + 50 * exp(- ((v + 40)^2]/(2 * 40^2))); if htau < 5 then htau = 5. The peak conductance for KA (gKA) 
was set to 0.0055 S/cm2, which corresponds to 1 nA potassium current at 0 mV.
ENDCOMMENT

UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX kas
    USEION k READ ek WRITE ik
    RANGE gbar, g, ik
    RANGE ninf, ntau, hinf, htau
	RANGE n, h
	RANGE tadj, q10
}

PARAMETER{ 
    gbar  = 0.0055 (S/cm2)
    q10    = 2.5 (1)
}

ASSIGNED {
	celsius (degC)
	tadj (1)

	v (mV)
    ik (mA/cm2)
    ek (mV)

    g (S/cm2)

    ninf (1)
    ntau (1/ms)

    hinf (1)
    htau (1/ms)
}

STATE{
    n h
}


UNITSOFF

INITIAL{
    tadj = q10^((celsius - 22) / 10)
    settables(v)
    n = ninf
    h = hinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    g = gbar * n * h
    ik = g * (v - ek)
}

DERIVATIVE states{
    settables(v)
    n' = (ninf - n) / ntau * tadj
    h' = (hinf - h) / htau * tadj
}


PROCEDURE settables(v (mV)){
    TABLE ninf, ntau, hinf, htau
    FROM -100 TO 100 WITH 200

    ninf   = 1 / (1 + exp(-(v + 5.4) / 16.4))^4
    ntau   = 0.25 + 10.04 * exp(-(v + 24.67)^2 / 2422.08)

    hinf   = 1 / (1 + exp((v + 49.9) / 4.6 ))
    htau   = 20 + 50 * exp(-(v + 40)^2 / 3200)

    if (htau < 5) {
        htau = 5
    }

}

UNITSON

