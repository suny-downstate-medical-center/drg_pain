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
    SUFFIX nav17
    USEION na READ ena WRITE ina
    RANGE gnabar, gna, ina
    RANGE minf, mtau 
    RANGE hinf, htau 
    RANGE sinf, stau 

    RANGE emut, rmut

    RANGE q10

}

PARAMETER{ 
    gnabar = 0.018 (S/cm2)
    emut   = 0
    rmut   = 0.0
:    q10    = 2.5
}

ASSIGNED {

	celsius (degC)
	v (mV)
    ina (mA/cm2)
    ena (mV)

    gna (S/cm2)

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

:    tadj (1)

}

STATE{
    m h s
}

UNITSOFF

INITIAL{
    settables(v)
:    tadj = q10 ^ (( celsius - 21) / 10)
    m = minf
    h = hinf
    s = sinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gna = gnabar * m^3 * h * s
    ina = gna * ((1 - rmut) * (v - ena) + (rmut * (v - emut)))
}

DERIVATIVE states{
    settables(v)
    m' = (minf-m)/mtau
    h' = (hinf-h)/htau
    s' = (sinf-s)/stau
}


PROCEDURE settables(v (mV)){
    TABLE minf, mtau, hinf, htau, sinf, stau
:    DEPEND celsius
    FROM -100 TO 100 WITH 200

    malpha = 15.5 / (1 + exp((v-5   ) / -12.08))
    mbeta  = 35.2 / (1 + exp((v+72.7) / 16.7))
    minf   = malpha / (malpha + mbeta)
    mtau   = 1 / (malpha + mbeta)
:    mtau   = 1 / (malpha + mbeta) / tadj    

    halpha =  0.38685           / ( 1 + exp( (v + 122.35) /  15.29   ))
    hbeta  = -0.00283 + 2.00283 / ( 1 + exp( (v + 5.5266) / -12.70195))
    hinf   = halpha / (halpha + hbeta)
    htau   = 1 / (halpha + hbeta)
:    htau   = 1 / (halpha + hbeta) / tadj    

    salpha = 0.00003 + 0.00092 / ( 1 + exp( (v + 93.9 ) / 16.6))
    sbeta  = 132.05  - 132.05  / ( 1 + exp( (v - 384.9) / 28.5))
    sinf   = salpha / (salpha + sbeta)
    stau   = 1 / (salpha + sbeta)
:    stau   = 1 / (salpha + sbeta) / tadj    

}

UNITSON
