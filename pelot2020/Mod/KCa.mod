: This channel is implemented by Nathan Titus 2019. 
: Calcium-Activated potassium channel of BK and SK Channel Contributions
: Kv7.2 (n) and Kv7.3 (m). Kv7.5 was considered "similar enough" to
: Kv7.2 so as to be considered a part of that current (n). 
: Data From:

NEURON {
	SUFFIX kcaNew
	USEION k READ ek WRITE ik
	USEION ca READ cai
	RANGE gbar, ek, ik
	RANGE tau_m,minf,ninf,tau_n,m,h,n,hinf,tau_h
	RANGE minfshift, hinfshift, ik, gp, g
}

UNITS {
	(S) = (siemens)
	(mV) = (millivolts)
	(mA) = (milliamp)
}

PARAMETER {
	gbar 	(S/cm2) 
	q10 = 3
        
    minfshift = 0 (mV)
	hinfshift = 0 (mV)
}

ASSIGNED {
	v	(mV) : NEURON provides this
	ik	(mA/cm2)
	g	(S/cm2)
	tau_m	(ms)
    tau_h  (ms)
    tau_n  (ms)
	cai		(mM)
    minf
	hinf
    ninf
	gp
    ek	(mV)
	celsius (degC)
}

STATE { n m h }

BREAKPOINT {
	SOLVE states METHOD cnexp
	gp = 0.9*m*h+0.1*n
	g = gbar*gp
	ik = g * (v-ek)
}

INITIAL {
	: assume that equilibrium has been reached
    rates(v)    
	m=minf :BK
    h=hinf :BK
    n=ninf :SK

}

DERIVATIVE states {
	rates(v)
	m' = (minf - m)/tau_m
	h' = (hinf - h)/tau_h
    n' = (ninf - n)/tau_n
          
}

? rates
PROCEDURE rates(Vm (mV)) (/ms) {    
	LOCAL Q10,v12,pca,vh12
UNITSOFF
		Q10 = q10^((celsius-22)/10)
		pca = log10(cai)-3 :converts to log10(cai [molar]) 
		
		:BK Component
		v12 =  -50*pca-232
		vh12 =  -8*pca+35
        minf= 1/(1+exp(-1*(Vm - v12)/24))
        hinf= 1/(1+exp((Vm - vh12)/47))
		tau_m = 1/(exp((Vm+(58*pca)+303)/(3.2*pca))+exp(-1*(Vm+(107*pca)+453)/(6.8*pca)))+0.4
		tau_h = 1/(exp((Vm+(3*pca)+100)/(3*pca))+exp(-1*(Vm+(191*pca)+600)/(17*pca)))
		
		:SK Component
		ninf= 1/(1+exp(-1*(pca + .4)/.12))
        tau_n = -1*pca :I was unable to find a value for this, but it should depend on concentration and be fairly fast
	
		
        tau_m=tau_m/Q10
        tau_h=tau_h/Q10
        tau_n=tau_n/Q10
UNITSON

}
