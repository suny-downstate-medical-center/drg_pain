TITLE KCNQ/M Current for bladder small DRG neuron soma model
: Adapted from Maingret et al., 2008

: For details refer: 
: A biophysically detailed computational model of bladder small DRG neuron soma 
: Darshan Mandge and Rohit Manchanda, PLOS Computational Biology (2018)

UNITS {
        (mA) = (milliamp)
        (mV) = (millivolt)
		(S) = (siemens)
}
 
NEURON {
        SUFFIX kmtype
        USEION k READ ek WRITE ik
        RANGE gbar, g, ik
        RANGE ninf, ntau
		RANGE n
		RANGE tadj, q10

		THREADSAFE
}

PARAMETER {
        gbar = 0.0001 (S/cm2)
		q10 = 2.5
}
 
STATE {
        n
}
 
ASSIGNED {
		celsius (degC)
		tadj (1)

		v (mV)
		ek (mV)

		g (S/cm2)
		ik (mA/cm2)

		ninf
		ntau (ms)	
}
 
BREAKPOINT {
        SOLVE states METHOD cnexp
        
        g = gbar*n
		ik = g*(v - ek)
}
 
 
INITIAL {
	tadj = q10 ^ ((celsius - 22) / 10)
	rates(v)
	n = ninf
}

DERIVATIVE states {  
        rates(v)
        n' = (ninf-n)/ntau * tadj
}
 

PROCEDURE rates(v(mV)) {
        LOCAL alpha, beta
	    TABLE ninf, ntau
	    FROM -100 TO 100 WITH 200
UNITSOFF
        :"n" potassium activation system
        ninf = (1/(1+exp(-(v+30)/6)))
        		
		alpha = 0.00395*exp((v+30)/40)
		beta  = 0.00395*exp(-(v+30)/20)
		ntau = 1/(alpha+beta)	
}
 
UNITSON
