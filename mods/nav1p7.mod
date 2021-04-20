COMMENT

Human WT NaV1.7 Channel 
reproduced from 
Sheets Et. Al (2007)

ENDCOMMENT

UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX nav1p7
    USEION na READ ena WRITE ina
    RANGE gbar, g, ina
    RANGE minf, mtau
    RANGE hinf, htau
    RANGE sinf, stau
	RANGE m, h, s
	RANGE tadj, q10

	RANGE ashft, ishft
}

PARAMETER{ 
    gbar = 0.018 (S/cm2)
	q10 = 2.5 (1)

	ashft = 0 (mV)
	ishft = 0 (mV)
}

ASSIGNED {
	celsius (degC)
	tadj (1)

	v (mV)
    ina (mA/cm2)
    ena (mV)

    g (S/cm2)

    malpha (1/ms)
    mbeta (1/ms)
    minf (1)
    mtau (ms) 

    halpha (1/ms)
    hbeta (1/ms)
    hinf (1)
    htau (ms)

    salpha (1/ms)
    sbeta (1/ms)
    sinf (1)
    stau (ms)
}

STATE{
    m h s
}

UNITSOFF

INITIAL{
	tadj = q10 ^ ((celsius - 22) / 10)
    settables(v)
    m = minf
    h = hinf
    s = sinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp

    g = gbar * m^3 * h * s
    ina = g * ( v - ena )
}

DERIVATIVE states{
    settables(v)
    m' = (minf-m)/mtau * tadj
    h' = (hinf-h)/htau * tadj
    s' = (sinf-s)/stau * tadj
}


PROCEDURE settables(v (mV)){
    TABLE minf, mtau, hinf, htau, sinf, stau
    DEPEND ashft, ishft
    FROM -100 TO 100 WITH 200

    malpha = 15.5 / (1 + exp( ( (v + ashft) - 5   ) / -12.08) )
    mbeta  = 35.2 / (1 + exp( ( (v + ashft) + 72.7) / 16.7) )
    minf   = malpha / (malpha + mbeta)
    mtau   = 1 / (malpha + mbeta)

    halpha =  0.38685           / ( 1 + exp( ( (v + ishft) + 122.35) /  15.29   ) )
    hbeta  = -0.00283 + 2.00283 / ( 1 + exp( ( (v + ishft) + 5.5266) / -12.70195) )
    hinf   = halpha / (halpha + hbeta)
    htau   = 1 / (halpha + hbeta)

    salpha = 0.00003 + 0.00092 / ( 1 + exp( ( (v + ishft) + 93.9 ) / 16.6) )
    sbeta  = 132.05  - 132.05  / ( 1 + exp( ( (v + ishft) - 384.9) / 28.5) )
    sinf   = salpha / (salpha + sbeta)
    stau   = 1 / (salpha + sbeta)
}

UNITSON
