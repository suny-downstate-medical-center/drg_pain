COMMENT

NaV1.8 Channel
Sheets et al. (2007)

ENDCOMMENT

UNITS {
    (mV) = (millivolt)
    (mA) = (milliamp)
    (S)  = (siemens)
}

NEURON {
    SUFFIX nav18
    USEION na READ ena WRITE ina
    RANGE gnabar, gna, ina
    RANGE minf, mtau
    RANGE hinf, htau
    RANGE sinf, stau
    RANGE uinf, utau
    RANGE emut, rmut

:    RANGE q10, tadj

}

PARAMETER{ 
    gnabar = 0.026 (S/cm2)
:    q10    = 2.5
    emut   = 0
    rmut   = 0

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

    ualpha (1/ms)
    ubeta (1/ms)
    uinf (1)
    utau (ms)

:    tadj

}

STATE{
    m h s u
}

UNITSOFF

INITIAL{
    settables(v)
:    tadj = q10^((celsius - 21) / 10)
    m = minf
    h = hinf
    s = sinf
    u = uinf
}

BREAKPOINT{
    SOLVE states METHOD cnexp
    
    gna = gnabar * m * m * m * h * s * u
    ina = gna * ((1 - rmut) * (v - ena) + (rmut * (v - emut)))
}

DERIVATIVE states{
    settables(v)
    m' = (minf-m)/mtau
    h' = (hinf-h)/htau
    s' = (sinf-s)/stau
    u' = (uinf-u)/utau
}

PROCEDURE settables(v (mV)){
    TABLE minf, mtau, hinf, htau
:    DEPEND celsius
    FROM -100 TO 100 WITH 200

    malpha = 2.85 - 2.839 / (1 + exp((v - 1.159) / 13.95))
    mbeta  = 7.6205 / (1 + exp((v + 46.463) / 8.8289))
    minf   = malpha / (malpha + mbeta)
    mtau   = 1 / (malpha + mbeta)
:    mtau   = 1 / (malpha + mbeta) / tadj

    hinf   = 1 / (1 + exp((v + 32.2) / 4))
    htau   = 1.218 + 42.043 * exp(-(v + 38.1)^2 / 461.4722)

    salpha = 0.001 * 5.4203 / (1 + exp((v + 79.816) / 16.269))
    sbeta  = 0.001 * 5.0757 / (1 + exp(-(v + 15.968 ) / 11.542))
    sinf   = 1 / ( 1 + exp((v + 45) / 8) )
    stau   = 1 / (salpha + sbeta)
:    stau   = 1 / (salpha + sbeta) / tadj

    ualpha = 0.0002 * 2.0434/ (1 + exp((v + 67.499) / 19.51))
    ubeta  = 0.0002 * 1.9952/( 1 + exp(-(v + 30.963) / 14.792))
    uinf   = 1 / ( 1 + exp((v + 51) / 8))
    utau   = 1 / (ualpha + ubeta)
:    utau   = 1 / (ualpha + ubeta) / tadj
 
}

UNITSON
